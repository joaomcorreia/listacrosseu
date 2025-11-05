"""
Management command to import businesses from Google Places API

Usage:
    python manage.py import_google_places --query "restaurants in Paris"
    python manage.py import_google_places --nearby "Paris, France" --type restaurant
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.services.google_places.importer import GooglePlacesImporter
import os


class Command(BaseCommand):
    help = 'Import businesses from Google Places API'

    def add_arguments(self, parser):
        # Query-based search arguments
        parser.add_argument(
            '--query',
            type=str,
            help='Search query (e.g., "restaurants in Paris")',
        )
        
        parser.add_argument(
            '--location',
            type=str,
            help='Location bias for query search (e.g., "Paris, France")',
        )
        
        parser.add_argument(
            '--region',
            type=str,
            help='Region code for query search (e.g., "fr")',
        )
        
        # Nearby search arguments
        parser.add_argument(
            '--nearby',
            type=str,
            help='Location for nearby search (e.g., "Paris, France")',
        )
        
        parser.add_argument(
            '--type',
            type=str,
            help='Place type for nearby search (e.g., "restaurant", "store")',
        )
        
        # General arguments
        parser.add_argument(
            '--user',
            type=str,
            help='Username of the user to assign imported businesses to',
        )
        
        parser.add_argument(
            '--api-key',
            type=str,
            help='Google Places API key (or set GOOGLE_PLACES_API_KEY env var)',
        )

    def handle(self, *args, **options):
        # Set API key if provided
        if options['api_key']:
            os.environ['GOOGLE_PLACES_API_KEY'] = options['api_key']
        
        # Validate that API key is available
        api_key = os.environ.get('GOOGLE_PLACES_API_KEY')
        if not api_key:
            self.stdout.write(
                self.style.ERROR(
                    'Google Places API key not found. Set GOOGLE_PLACES_API_KEY environment variable or use --api-key option.'
                )
            )
            return
        
        # Get user for import
        user = None
        if options['user']:
            try:
                user = User.objects.get(username=options['user'])
                self.stdout.write(f"Using user: {user.username}")
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"User '{options['user']}' not found")
                )
                return
        
        # Initialize importer
        try:
            importer = GooglePlacesImporter(user=user)
        except ValueError as e:
            self.stdout.write(self.style.ERROR(str(e)))
            return
        
        # Determine import type and execute
        if options['query']:
            self._import_by_query(importer, options)
        elif options['nearby']:
            self._import_nearby(importer, options)
        else:
            self.stdout.write(
                self.style.ERROR(
                    'Please specify either --query for query-based search or --nearby for nearby search.'
                )
            )
    
    def _import_by_query(self, importer, options):
        """Execute query-based import"""
        query = options['query']
        location = options.get('location')
        region = options.get('region')
        
        self.stdout.write(f"🔍 Searching Google Places for: {query}")
        if location:
            self.stdout.write(f"📍 Location bias: {location}")
        if region:
            self.stdout.write(f"🌍 Region: {region}")
        
        # Execute import
        results = importer.import_by_query(query, location, region)
        
        # Display results
        self._display_results(results)
        
        # Show progress if available
        progress = importer.get_progress()
        if progress.get('message'):
            self.stdout.write(f"📊 Final status: {progress['message']}")
    
    def _import_nearby(self, importer, options):
        """Execute nearby search import"""
        location = options['nearby']
        place_type = options.get('type')
        
        self.stdout.write(f"🗺️ Searching nearby places in: {location}")
        if place_type:
            self.stdout.write(f"🏪 Place type: {place_type}")
        
        # Execute import
        results = importer.import_nearby(location, place_type)
        
        # Display results
        self._display_results(results)
        
        # Show progress if available
        progress = importer.get_progress()
        if progress.get('message'):
            self.stdout.write(f"📊 Final status: {progress['message']}")
    
    def _display_results(self, results):
        """Display import results"""
        if results['success']:
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Import completed successfully!"
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    f"❌ Import failed: {results.get('message', 'Unknown error')}"
                )
            )
        
        # Display statistics
        self.stdout.write(f"📈 Import Statistics:")
        self.stdout.write(f"  • Imported: {results.get('imported', 0)} businesses")
        self.stdout.write(f"  • Skipped: {results.get('skipped', 0)} (already exist)")
        self.stdout.write(f"  • Errors: {results.get('errors', 0)}")
        
        if results.get('message'):
            self.stdout.write(f"💬 Message: {results['message']}")