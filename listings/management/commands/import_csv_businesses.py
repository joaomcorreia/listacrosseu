"""
Django management command to import businesses from CSV files
Usage: python manage.py import_csv_businesses path/to/file.csv
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.files import File
from listings.models import CSVUpload
from listings.services.csv_processor import process_csv_upload
import os


class Command(BaseCommand):
    help = 'Import businesses from a CSV file'
    
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file to import')
        parser.add_argument(
            '--user',
            type=str,
            help='Username of the user to associate with this import (default: first superuser)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Validate CSV without importing data'
        )
    
    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        username = options.get('user')
        dry_run = options['dry_run']
        
        # Check if file exists
        if not os.path.exists(csv_file_path):
            raise CommandError(f'File "{csv_file_path}" does not exist.')
        
        if not csv_file_path.endswith('.csv'):
            raise CommandError('File must be a CSV file (.csv extension)')
        
        # Get user for the import
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise CommandError(f'User "{username}" does not exist.')
        else:
            user = User.objects.filter(is_superuser=True).first()
            if not user:
                raise CommandError('No superuser found. Please create a superuser first.')
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE - No data will be imported')
            )
        
        try:
            # Create CSV upload record
            with open(csv_file_path, 'rb') as f:
                csv_upload = CSVUpload.objects.create(
                    file=File(f, name=os.path.basename(csv_file_path)),
                    uploaded_by=user
                )
            
            self.stdout.write(f'Processing CSV file: {csv_file_path}')
            self.stdout.write(f'Upload ID: {csv_upload.id}')
            self.stdout.write(f'Uploaded by: {user.username}')
            
            if not dry_run:
                # Process the CSV file
                result = process_csv_upload(csv_upload.id)
                
                if result['success']:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✓ Successfully processed CSV file!'
                        )
                    )
                    self.stdout.write(f'  • Total businesses imported: {result["successful_count"]}')
                    if result['failed_count'] > 0:
                        self.stdout.write(
                            self.style.WARNING(
                                f'  • Failed rows: {result["failed_count"]}'
                            )
                        )
                        if result['errors']:
                            self.stdout.write('  • Errors:')
                            for error in result['errors'][:5]:  # Show first 5 errors
                                self.stdout.write(f'    - {error}')
                            if len(result['errors']) > 5:
                                self.stdout.write(f'    ... and {len(result["errors"]) - 5} more errors')
                else:
                    self.stdout.write(
                        self.style.ERROR(f'✗ Failed to process CSV: {result["message"]}')
                    )
                    return
            else:
                # For dry run, just validate the file can be read
                from listings.services.csv_processor import CSVBusinessProcessor
                processor = CSVBusinessProcessor(csv_upload)
                try:
                    csv_data = processor._read_csv_file()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✓ CSV file is valid and contains {len(csv_data)} rows'
                        )
                    )
                    
                    # Show sample of what would be imported
                    if csv_data:
                        self.stdout.write('\\nSample data (first row):')
                        sample_row = csv_data[0]
                        for key, value in sample_row.items():
                            if value:  # Only show non-empty values
                                self.stdout.write(f'  {key}: {value[:50]}{"..." if len(str(value)) > 50 else ""}')
                
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'✗ CSV validation failed: {str(e)}')
                    )
                    # Clean up the upload record since it failed
                    csv_upload.delete()
                    return
                
                # Clean up the upload record for dry run
                csv_upload.delete()
            
            self.stdout.write('\\nDone!')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )
            raise CommandError(f'Import failed: {str(e)}')