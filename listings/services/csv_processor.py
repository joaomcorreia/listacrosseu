"""
CSV Upload Processing Service for Business Data
"""
import csv
import logging
from typing import Dict, List, Tuple, Any
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from django.db import transaction
from listings.models import Business, Category, CSVUpload

logger = logging.getLogger(__name__)


class CSVBusinessProcessor:
    """Service class to process CSV files containing business data"""
    
    # Define expected CSV columns and their mapping to model fields
    CSV_FIELD_MAPPING = {
        'name': 'name',
        'business_name': 'name',
        'description': 'description',
        'address': 'address',
        'phone': 'phone',
        'phone_number': 'phone',
        'website': 'website',
        'website_url': 'website',
        'email': 'email',
        'category': 'category',
        'business_category': 'category',
        'city': 'city',
        'country': 'country',
        'postal_code': 'postal_code',
        'zip_code': 'postal_code',
        'latitude': 'latitude',
        'longitude': 'longitude',
        'monday_hours': 'monday_hours',
        'tuesday_hours': 'tuesday_hours',
        'wednesday_hours': 'wednesday_hours',
        'thursday_hours': 'thursday_hours',
        'friday_hours': 'friday_hours',
        'saturday_hours': 'saturday_hours',
        'sunday_hours': 'sunday_hours',
        'is_active': 'is_active',
        'is_public': 'is_public',
        'is_featured': 'is_featured',
    }
    
    def __init__(self, csv_upload: CSVUpload):
        self.csv_upload = csv_upload
        self.errors = []
        self.successful_count = 0
        self.failed_count = 0
    
    def process_csv(self) -> Tuple[int, int, List[str]]:
        """
        Process the uploaded CSV file and create Business entries
        Returns: (successful_count, failed_count, errors)
        """
        try:
            # Mark as processing
            self.csv_upload.mark_as_processing()
            
            # Read and validate CSV file
            csv_data = self._read_csv_file()
            if not csv_data:
                raise Exception("Could not read CSV file or file is empty")
            
            # Count total rows for progress tracking
            self.csv_upload.total_rows = len(csv_data)
            self.csv_upload.save()
            
            # Process each row
            for row_index, row_data in enumerate(csv_data, start=1):
                try:
                    with transaction.atomic():
                        self._process_single_row(row_data, row_index)
                        self.successful_count += 1
                except Exception as e:
                    self.failed_count += 1
                    error_msg = f"Row {row_index}: {str(e)}"
                    self.errors.append(error_msg)
                    logger.error(f"CSV Processing Error - {error_msg}")
            
            # Mark as completed
            self.csv_upload.mark_as_completed(self.successful_count, self.failed_count)
            if self.errors:
                self.csv_upload.error_log = "\\n".join(self.errors)
                self.csv_upload.save()
            
            return self.successful_count, self.failed_count, self.errors
            
        except Exception as e:
            # Mark as failed
            error_message = f"CSV Processing Failed: {str(e)}"
            self.csv_upload.mark_as_failed(error_message)
            logger.error(error_message)
            return 0, 0, [error_message]
    
    def _read_csv_file(self) -> List[Dict[str, Any]]:
        """Read CSV file and return list of dictionaries"""
        csv_data = []
        
        try:
            # Open and read the CSV file
            with open(self.csv_upload.file.path, 'r', encoding='utf-8') as file:
                # Try to detect delimiter
                sample = file.read(1024)
                file.seek(0)
                
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter
                
                reader = csv.DictReader(file, delimiter=delimiter)
                
                # Normalize column names (lowercase, replace spaces with underscores)
                normalized_fieldnames = []
                for field in reader.fieldnames:
                    normalized_field = field.lower().strip().replace(' ', '_').replace('-', '_')
                    normalized_fieldnames.append(normalized_field)
                
                # Process each row
                for row in reader:
                    # Create normalized row data
                    normalized_row = {}
                    for original_field, normalized_field in zip(reader.fieldnames, normalized_fieldnames):
                        normalized_row[normalized_field] = row[original_field]
                    
                    csv_data.append(normalized_row)
            
            return csv_data
            
        except Exception as e:
            logger.error(f"Error reading CSV file: {str(e)}")
            raise Exception(f"Could not read CSV file: {str(e)}")
    
    def _process_single_row(self, row_data: Dict[str, Any], row_index: int):
        """Process a single CSV row and create a Business entry"""
        
        # Extract and validate required fields
        business_name = self._get_mapped_value(row_data, 'name')
        if not business_name:
            raise Exception("Business name is required")
        
        # Generate unique slug
        base_slug = slugify(business_name)
        slug = base_slug
        counter = 1
        while Business.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        # Get or create category
        category_name = self._get_mapped_value(row_data, 'category')
        category = None
        if category_name:
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={'slug': slugify(category_name)}
            )
        
        # Get default owner (first superuser or create system user)
        owner = self._get_default_owner()
        
        # Prepare business data
        business_data = {
            'name': business_name,
            'slug': slug,
            'description': self._get_mapped_value(row_data, 'description') or '',
            'address': self._get_mapped_value(row_data, 'address') or '',
            'phone': self._get_mapped_value(row_data, 'phone') or '',
            'email': self._get_mapped_value(row_data, 'email') or '',
            'website': self._get_mapped_value(row_data, 'website') or '',
            'city': self._get_mapped_value(row_data, 'city') or '',
            'country': self._get_mapped_value(row_data, 'country') or '',
            'postal_code': self._get_mapped_value(row_data, 'postal_code') or '',
            'category': category,
            'owner': owner,
            'imported_from_csv': True,
            'csv_import_date': timezone.now(),
        }
        
        # Add opening hours
        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            hours_field = f"{day}_hours"
            hours_value = self._get_mapped_value(row_data, hours_field)
            if hours_value:
                business_data[hours_field] = hours_value
        
        # Add coordinates if available
        latitude = self._get_mapped_value(row_data, 'latitude')
        longitude = self._get_mapped_value(row_data, 'longitude')
        if latitude and longitude:
            try:
                business_data['latitude'] = float(latitude)
                business_data['longitude'] = float(longitude)
            except ValueError:
                pass  # Skip invalid coordinates
        
        # Add boolean fields
        is_active = self._get_mapped_value(row_data, 'is_active')
        if is_active is not None:
            business_data['is_active'] = self._parse_boolean(is_active)
        
        is_public = self._get_mapped_value(row_data, 'is_public')
        if is_public is not None:
            business_data['is_public'] = self._parse_boolean(is_public)
        
        is_featured = self._get_mapped_value(row_data, 'is_featured')
        if is_featured is not None:
            business_data['is_featured'] = self._parse_boolean(is_featured)
        
        # Create the business entry
        business = Business.objects.create(**business_data)
        
        logger.info(f"Successfully created business: {business.name} (ID: {business.id})")
        
        return business
    
    def _get_mapped_value(self, row_data: Dict[str, Any], field_name: str) -> Any:
        """Get value from row data using field mapping"""
        # Try to find the field using mapping
        for csv_field, mapped_field in self.CSV_FIELD_MAPPING.items():
            if mapped_field == field_name and csv_field in row_data:
                value = row_data[csv_field]
                # Clean up the value
                if isinstance(value, str):
                    value = value.strip()
                    if value == '':
                        return None
                return value
        return None
    
    def _parse_boolean(self, value: Any) -> bool:
        """Parse various boolean representations"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            value = value.lower().strip()
            return value in ['true', '1', 'yes', 'y', 'on', 'active']
        if isinstance(value, (int, float)):
            return bool(value)
        return False
    
    def _get_default_owner(self) -> User:
        """Get default owner for imported businesses"""
        # Try to use the user who uploaded the CSV
        if self.csv_upload.uploaded_by:
            return self.csv_upload.uploaded_by
        
        # Fallback to first superuser
        superuser = User.objects.filter(is_superuser=True).first()
        if superuser:
            return superuser
        
        # Create system user if none exists
        system_user, created = User.objects.get_or_create(
            username='csv_import_system',
            defaults={
                'email': 'system@listacrosseu.com',
                'first_name': 'CSV Import',
                'last_name': 'System',
                'is_active': True,
            }
        )
        return system_user


def process_csv_upload(csv_upload_id: int) -> Dict[str, Any]:
    """
    Process a CSV upload by ID
    Can be called from admin actions or background tasks
    """
    try:
        csv_upload = CSVUpload.objects.get(id=csv_upload_id)
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
        logger.error(f"Error processing CSV upload {csv_upload_id}: {str(e)}")
        return {
            'success': False,
            'message': f"Processing failed: {str(e)}"
        }