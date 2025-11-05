"""
Optimized CSV Processing Service for Large Files
Handles batch processing, progress tracking, and memory optimization
"""
import csv
import logging
from typing import Dict, List, Tuple, Any, Generator
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from django.db import transaction
from django.core.cache import cache
from listings.models import Business, Category, CSVUpload
from concurrent.futures import ThreadPoolExecutor
import time

logger = logging.getLogger(__name__)


class LargeCSVProcessor:
    """Optimized processor for large CSV files with batch processing and progress tracking"""
    
    BATCH_SIZE = 100  # Process in batches of 100 rows
    MAX_WORKERS = 4   # Number of concurrent processing threads
    PROGRESS_UPDATE_INTERVAL = 50  # Update progress every 50 rows
    
    def __init__(self, csv_upload: CSVUpload):
        self.csv_upload = csv_upload
        self.errors = []
        self.successful_count = 0
        self.failed_count = 0
        self.progress_cache_key = f"csv_progress_{csv_upload.id}"
    
    def process_csv_chunked(self) -> Tuple[int, int, List[str]]:
        """
        Process large CSV files in chunks with progress tracking
        Returns: (successful_count, failed_count, errors)
        """
        try:
            # Mark as processing
            self.csv_upload.mark_as_processing()
            self._update_progress(0, "Starting CSV processing...")
            
            # Count total rows first (without loading into memory)
            total_rows = self._count_csv_rows()
            self.csv_upload.total_rows = total_rows
            self.csv_upload.save()
            
            logger.info(f"Processing large CSV with {total_rows} rows in batches of {self.BATCH_SIZE}")
            
            # Process in batches
            processed_rows = 0
            for batch_data in self._read_csv_in_batches():
                batch_successful, batch_failed = self._process_batch(batch_data, processed_rows)
                
                self.successful_count += batch_successful
                self.failed_count += batch_failed
                processed_rows += len(batch_data)
                
                # Update progress
                progress_pct = (processed_rows / total_rows) * 100
                self._update_progress(
                    progress_pct, 
                    f"Processed {processed_rows}/{total_rows} rows. Success: {self.successful_count}, Failed: {self.failed_count}"
                )
                
                # Small delay to prevent overwhelming the database
                time.sleep(0.1)
            
            # Mark as completed
            self.csv_upload.mark_as_completed(self.successful_count, self.failed_count)
            if self.errors:
                # Limit error log size for large files
                error_summary = self.errors[:100] if len(self.errors) > 100 else self.errors
                if len(self.errors) > 100:
                    error_summary.append(f"... and {len(self.errors) - 100} more errors")
                self.csv_upload.error_log = "\\n".join(error_summary)
                self.csv_upload.save()
            
            self._update_progress(100, f"Completed! {self.successful_count} imported, {self.failed_count} failed")
            
            return self.successful_count, self.failed_count, self.errors
            
        except Exception as e:
            error_message = f"Large CSV Processing Failed: {str(e)}"
            self.csv_upload.mark_as_failed(error_message)
            self._update_progress(0, f"Failed: {error_message}")
            logger.error(error_message)
            return 0, 0, [error_message]
    
    def _count_csv_rows(self) -> int:
        """Count total rows in CSV without loading into memory"""
        try:
            with open(self.csv_upload.file.path, 'r', encoding='utf-8') as file:
                # Skip header row
                next(csv.reader(file))
                return sum(1 for _ in csv.reader(file))
        except Exception as e:
            logger.error(f"Error counting CSV rows: {str(e)}")
            return 0
    
    def _read_csv_in_batches(self) -> Generator[List[Dict[str, Any]], None, None]:
        """Generator that yields batches of CSV data"""
        try:
            with open(self.csv_upload.file.path, 'r', encoding='utf-8') as file:
                # Detect delimiter
                sample = file.read(1024)
                file.seek(0)
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter
                
                reader = csv.DictReader(file, delimiter=delimiter)
                
                # Normalize field names
                normalized_fieldnames = []
                for field in reader.fieldnames:
                    normalized_field = field.lower().strip().replace(' ', '_').replace('-', '_')
                    normalized_fieldnames.append(normalized_field)
                
                batch = []
                for row in reader:
                    # Create normalized row
                    normalized_row = {}
                    for original_field, normalized_field in zip(reader.fieldnames, normalized_fieldnames):
                        normalized_row[normalized_field] = row[original_field]
                    
                    batch.append(normalized_row)
                    
                    # Yield batch when it reaches the batch size
                    if len(batch) >= self.BATCH_SIZE:
                        yield batch
                        batch = []
                
                # Yield remaining rows
                if batch:
                    yield batch
                    
        except Exception as e:
            logger.error(f"Error reading CSV in batches: {str(e)}")
            raise Exception(f"Could not read CSV file: {str(e)}")
    
    def _process_batch(self, batch_data: List[Dict[str, Any]], start_row: int) -> Tuple[int, int]:
        """Process a batch of CSV rows with bulk operations"""
        batch_successful = 0
        batch_failed = 0
        
        # Prepare businesses for bulk creation
        businesses_to_create = []
        categories_cache = {}
        
        for row_index, row_data in enumerate(batch_data, start=start_row + 1):
            try:
                business_data = self._prepare_business_data(row_data, row_index, categories_cache)
                if business_data:
                    businesses_to_create.append(Business(**business_data))
                    batch_successful += 1
            except Exception as e:
                batch_failed += 1
                error_msg = f"Row {row_index}: {str(e)}"
                self.errors.append(error_msg)
                logger.error(f"CSV Processing Error - {error_msg}")
        
        # Bulk create businesses
        if businesses_to_create:
            try:
                with transaction.atomic():
                    Business.objects.bulk_create(businesses_to_create, ignore_conflicts=True)
                    logger.info(f"Bulk created {len(businesses_to_create)} businesses")
            except Exception as e:
                # If bulk create fails, fall back to individual creation
                logger.warning(f"Bulk create failed, falling back to individual creation: {str(e)}")
                batch_successful, batch_failed = self._process_batch_individually(batch_data, start_row)
        
        return batch_successful, batch_failed
    
    def _process_batch_individually(self, batch_data: List[Dict[str, Any]], start_row: int) -> Tuple[int, int]:
        """Fallback: process batch items individually if bulk creation fails"""
        batch_successful = 0
        batch_failed = 0
        categories_cache = {}
        
        for row_index, row_data in enumerate(batch_data, start=start_row + 1):
            try:
                with transaction.atomic():
                    business_data = self._prepare_business_data(row_data, row_index, categories_cache)
                    if business_data:
                        Business.objects.create(**business_data)
                        batch_successful += 1
            except Exception as e:
                batch_failed += 1
                error_msg = f"Row {row_index}: {str(e)}"
                self.errors.append(error_msg)
                logger.error(f"CSV Processing Error - {error_msg}")
        
        return batch_successful, batch_failed
    
    def _prepare_business_data(self, row_data: Dict[str, Any], row_index: int, categories_cache: Dict) -> Dict[str, Any]:
        """Prepare business data for creation (same as original but with caching)"""
        from listings.services.csv_processor import CSVBusinessProcessor
        
        # Use the original field mapping logic
        processor = CSVBusinessProcessor(self.csv_upload)
        
        # Extract and validate required fields
        business_name = processor._get_mapped_value(row_data, 'name')
        if not business_name:
            raise Exception("Business name is required")
        
        # Generate unique slug with better collision handling
        base_slug = slugify(business_name)
        slug = self._get_unique_slug(base_slug, row_index)
        
        # Get or create category with caching
        category_name = processor._get_mapped_value(row_data, 'category')
        category = None
        if category_name:
            if category_name not in categories_cache:
                category, created = Category.objects.get_or_create(
                    name=category_name,
                    defaults={'slug': slugify(category_name)}
                )
                categories_cache[category_name] = category
            else:
                category = categories_cache[category_name]
        
        # Get default owner
        owner = processor._get_default_owner()
        
        # Prepare business data (same as original)
        business_data = {
            'name': business_name,
            'slug': slug,
            'description': processor._get_mapped_value(row_data, 'description') or '',
            'address': processor._get_mapped_value(row_data, 'address') or '',
            'phone': processor._get_mapped_value(row_data, 'phone') or '',
            'email': processor._get_mapped_value(row_data, 'email') or '',
            'website': processor._get_mapped_value(row_data, 'website') or '',
            'city': processor._get_mapped_value(row_data, 'city') or '',
            'country': processor._get_mapped_value(row_data, 'country') or '',
            'postal_code': processor._get_mapped_value(row_data, 'postal_code') or '',
            'category': category,
            'owner': owner,
            'imported_from_csv': True,
            'csv_import_date': timezone.now(),
        }
        
        # Add opening hours
        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            hours_field = f"{day}_hours"
            hours_value = processor._get_mapped_value(row_data, hours_field)
            if hours_value:
                business_data[hours_field] = hours_value
        
        # Add coordinates if available
        latitude = processor._get_mapped_value(row_data, 'latitude')
        longitude = processor._get_mapped_value(row_data, 'longitude')
        if latitude and longitude:
            try:
                business_data['latitude'] = float(latitude)
                business_data['longitude'] = float(longitude)
            except ValueError:
                pass  # Skip invalid coordinates
        
        # Add boolean fields
        is_active = processor._get_mapped_value(row_data, 'is_active')
        if is_active is not None:
            business_data['is_active'] = processor._parse_boolean(is_active)
        
        is_public = processor._get_mapped_value(row_data, 'is_public')
        if is_public is not None:
            business_data['is_public'] = processor._parse_boolean(is_public)
        
        is_featured = processor._get_mapped_value(row_data, 'is_featured')
        if is_featured is not None:
            business_data['is_featured'] = processor._parse_boolean(is_featured)
        
        return business_data
    
    def _get_unique_slug(self, base_slug: str, row_index: int) -> str:
        """Generate unique slug with better performance for large datasets"""
        # For large imports, use row index to reduce collision checks
        slug = f"{base_slug}-{row_index}" if Business.objects.filter(slug=base_slug).exists() else base_slug
        
        # Double-check uniqueness
        counter = 1
        original_slug = slug
        while Business.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        return slug
    
    def _update_progress(self, percentage: float, message: str):
        """Update processing progress in cache"""
        progress_data = {
            'percentage': round(percentage, 2),
            'message': message,
            'successful_count': self.successful_count,
            'failed_count': self.failed_count,
            'timestamp': timezone.now().isoformat()
        }
        
        # Cache progress for 1 hour
        cache.set(self.progress_cache_key, progress_data, 3600)
        
        logger.info(f"CSV Progress: {percentage:.1f}% - {message}")
    
    def get_progress(self) -> Dict[str, Any]:
        """Get current processing progress"""
        return cache.get(self.progress_cache_key, {
            'percentage': 0,
            'message': 'Processing not started',
            'successful_count': 0,
            'failed_count': 0,
            'timestamp': timezone.now().isoformat()
        })


def process_large_csv_upload(csv_upload_id: int) -> Dict[str, Any]:
    """
    Process large CSV uploads with optimized batch processing
    """
    try:
        csv_upload = CSVUpload.objects.get(id=csv_upload_id)
        
        # Check file size and choose appropriate processor
        file_size = csv_upload.file.size
        if file_size > 1024 * 1024:  # Files larger than 1MB use optimized processor
            processor = LargeCSVProcessor(csv_upload)
            successful, failed, errors = processor.process_csv_chunked()
        else:
            # Use original processor for small files
            from listings.services.csv_processor import CSVBusinessProcessor
            processor = CSVBusinessProcessor(csv_upload)
            successful, failed, errors = processor.process_csv()
        
        return {
            'success': True,
            'successful_count': successful,
            'failed_count': failed,
            'errors': errors,
            'message': f"Processing completed: {successful} successful, {failed} failed"
        }
    
    except CSVUpload.DoesNotExist:
        return {
            'success': False,
            'message': f"CSV Upload with ID {csv_upload_id} not found"
        }
    except Exception as e:
        logger.error(f"Error processing large CSV upload {csv_upload_id}: {str(e)}")
        return {
            'success': False,
            'message': f"Processing failed: {str(e)}"
        }