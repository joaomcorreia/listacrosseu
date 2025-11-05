"""
Django management command for importing large CSV files with progress tracking
Usage: python manage.py import_large_csv path/to/file.csv
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.files import File
from listings.models import CSVUpload
from listings.services.large_csv_processor import process_large_csv_upload, LargeCSVProcessor
import os
import time
import threading


class Command(BaseCommand):
    help = 'Import large CSV files with optimized batch processing'
    
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file to import')
        parser.add_argument(
            '--user',
            type=str,
            help='Username of the user to associate with this import (default: first superuser)'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='Number of rows to process in each batch (default: 100)'
        )
        parser.add_argument(
            '--progress',
            action='store_true',
            help='Show real-time progress updates'
        )
        parser.add_argument(
            '--async',
            action='store_true',
            dest='async_mode',
            help='Process in background with progress monitoring'
        )
    
    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        username = options.get('user')
        batch_size = options['batch_size']
        show_progress = options['progress']
        async_mode = options['async_mode']
        
        # Validate file
        if not os.path.exists(csv_file_path):
            raise CommandError(f'File "{csv_file_path}" does not exist.')
        
        if not csv_file_path.endswith('.csv'):
            raise CommandError('File must be a CSV file (.csv extension)')
        
        # Check file size
        file_size = os.path.getsize(csv_file_path)
        file_size_mb = file_size / (1024 * 1024)
        
        self.stdout.write(f'File size: {file_size_mb:.1f} MB')
        
        if file_size_mb > 10:
            self.stdout.write(
                self.style.WARNING(
                    f'Large file detected ({file_size_mb:.1f} MB). Using optimized batch processing.'
                )
            )
        
        # Get user
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise CommandError(f'User "{username}" does not exist.')
        else:
            user = User.objects.filter(is_superuser=True).first()
            if not user:
                raise CommandError('No superuser found. Please create a superuser first.')
        
        # Create upload record
        try:
            with open(csv_file_path, 'rb') as f:
                csv_upload = CSVUpload.objects.create(
                    file=File(f, name=os.path.basename(csv_file_path)),
                    uploaded_by=user
                )
            
            self.stdout.write(f'Created upload record with ID: {csv_upload.id}')
            self.stdout.write(f'File: {csv_file_path}')
            self.stdout.write(f'Batch size: {batch_size}')
            self.stdout.write(f'Uploaded by: {user.username}')
            
            if async_mode:
                self._process_async(csv_upload.id, show_progress)
            else:
                self._process_sync(csv_upload.id, show_progress)
                
        except Exception as e:
            raise CommandError(f'Import failed: {str(e)}')
    
    def _process_sync(self, csv_upload_id: int, show_progress: bool):
        """Process CSV synchronously with optional progress monitoring"""
        
        if show_progress:
            # Start progress monitoring in a separate thread
            progress_thread = threading.Thread(
                target=self._monitor_progress,
                args=(csv_upload_id,),
                daemon=True
            )
            progress_thread.start()
        
        self.stdout.write('Starting CSV processing...')
        start_time = time.time()
        
        # Process the CSV
        result = process_large_csv_upload(csv_upload_id)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        if result['success']:
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Processing completed in {processing_time:.1f} seconds!'
                )
            )
            self.stdout.write(f'  • Successfully imported: {result["successful_count"]} businesses')
            if result['failed_count'] > 0:
                self.stdout.write(
                    self.style.WARNING(
                        f'  • Failed rows: {result["failed_count"]}'
                    )
                )
            
            # Show performance stats
            if result['successful_count'] > 0:
                rate = result['successful_count'] / processing_time
                self.stdout.write(f'  • Processing rate: {rate:.1f} businesses/second')
        else:
            self.stdout.write(
                self.style.ERROR(f'✗ Processing failed: {result["message"]}')
            )
    
    def _process_async(self, csv_upload_id: int, show_progress: bool):
        """Process CSV asynchronously with progress monitoring"""
        
        self.stdout.write('Starting background CSV processing...')
        self.stdout.write('Use Ctrl+C to exit monitoring (processing will continue)')
        
        # Start processing in background thread
        def background_process():
            process_large_csv_upload(csv_upload_id)
        
        process_thread = threading.Thread(target=background_process, daemon=True)
        process_thread.start()
        
        # Monitor progress
        try:
            self._monitor_progress(csv_upload_id, continuous=True)
        except KeyboardInterrupt:
            self.stdout.write('\\nExiting progress monitor. Processing continues in background.')
            self.stdout.write(f'Check upload status with: python manage.py csv_status {csv_upload_id}')
    
    def _monitor_progress(self, csv_upload_id: int, continuous: bool = False):
        """Monitor processing progress"""
        csv_upload = CSVUpload.objects.get(id=csv_upload_id)
        processor = LargeCSVProcessor(csv_upload)
        
        last_percentage = -1
        
        while True:
            progress = processor.get_progress()
            percentage = progress.get('percentage', 0)
            message = progress.get('message', 'Processing...')
            
            # Only update if percentage changed significantly
            if abs(percentage - last_percentage) >= 1 or percentage == 100:
                self.stdout.write(f'\\r[{percentage:6.1f}%] {message}', ending='')
                self.stdout.flush()
                last_percentage = percentage
            
            # Check if completed
            csv_upload.refresh_from_db()
            if csv_upload.status in ['completed', 'failed']:
                self.stdout.write(f'\\nFinal status: {csv_upload.status}')
                break
            
            if not continuous:
                time.sleep(1)
                # For sync mode, just show progress a few times
                if percentage > 50:  # Stop monitoring after halfway point
                    break
            else:
                time.sleep(2)  # Update every 2 seconds for async mode