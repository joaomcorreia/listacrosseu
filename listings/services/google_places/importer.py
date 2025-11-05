"""
Google Places Import Service

This service handles importing businesses from Google Places API
and saving them to the database with progress tracking.
"""

import logging
from typing import List, Dict, Optional
from django.db import transaction
from django.core.cache import cache
from django.utils import timezone
from django.contrib.auth.models import User
from listings.models import Business, Category
from listings.services.google_places.places_api import GooglePlacesService

logger = logging.getLogger(__name__)


class GooglePlacesImporter:
    """Service for importing and processing Google Places data"""
    
    def __init__(self, user: User = None):
        """Initialize the importer with optional user context"""
        self.places_service = GooglePlacesService()
        self.user = user or self._get_default_user()
        self.progress_key = None
    
    def _get_default_user(self) -> User:
        """Get or create a default user for Google Places imports"""
        user, created = User.objects.get_or_create(
            username='google_places_importer',
            defaults={
                'email': 'system@listacrosseu.com',
                'first_name': 'Google Places',
                'last_name': 'Importer',
                'is_active': False,  # System user
            }
        )
        return user
    
    def import_by_query(self, query: str, location: str = None, region: str = None) -> Dict:
        """
        Import businesses by search query
        
        Args:
            query: Search query (e.g., "restaurants in Paris")
            location: Optional location bias
            region: Optional region code
            
        Returns:
            Dictionary with import results
        """
        import_id = f"google_places_query_{timezone.now().timestamp()}"
        self.progress_key = f"google_places_import_{import_id}"
        
        try:
            self._update_progress(0, 0, 0, "Starting Google Places search...")
            
            # Search for places
            places = self.places_service.search_places_by_query(query, location, region)
            
            if not places:
                self._update_progress(0, 0, 0, "No places found for query")
                return {
                    'success': True,
                    'imported': 0,
                    'skipped': 0,
                    'errors': 0,
                    'message': 'No places found for the given query'
                }
            
            self._update_progress(0, len(places), 0, f"Found {len(places)} places. Starting import...")
            
            # Import the places
            results = self._import_places_list(places)
            
            self._update_progress(
                results['imported'] + results['skipped'] + results['errors'],
                len(places),
                0,
                f"Import completed: {results['imported']} imported, {results['skipped']} skipped, {results['errors']} errors"
            )
            
            return results
            
        except Exception as e:
            logger.error(f"Error in Google Places import by query: {e}")
            self._update_progress(0, 0, 1, f"Import failed: {str(e)}")
            return {
                'success': False,
                'imported': 0,
                'skipped': 0,
                'errors': 1,
                'message': f'Import failed: {str(e)}'
            }
    
    def import_nearby(self, location: str, place_type: str = None) -> Dict:
        """
        Import businesses near a location
        
        Args:
            location: Location to search near
            place_type: Optional place type filter
            
        Returns:
            Dictionary with import results
        """
        import_id = f"google_places_nearby_{timezone.now().timestamp()}"
        self.progress_key = f"google_places_import_{import_id}"
        
        try:
            self._update_progress(0, 0, 0, f"Searching nearby places in {location}...")
            
            # Search for nearby places
            places = self.places_service.search_places_nearby(location, place_type)
            
            if not places:
                self._update_progress(0, 0, 0, "No nearby places found")
                return {
                    'success': True,
                    'imported': 0,
                    'skipped': 0,
                    'errors': 0,
                    'message': 'No nearby places found'
                }
            
            self._update_progress(0, len(places), 0, f"Found {len(places)} nearby places. Starting import...")
            
            # Import the places
            results = self._import_places_list(places)
            
            self._update_progress(
                results['imported'] + results['skipped'] + results['errors'],
                len(places),
                0,
                f"Import completed: {results['imported']} imported, {results['skipped']} skipped, {results['errors']} errors"
            )
            
            return results
            
        except Exception as e:
            logger.error(f"Error in Google Places nearby import: {e}")
            self._update_progress(0, 0, 1, f"Import failed: {str(e)}")
            return {
                'success': False,
                'imported': 0,
                'skipped': 0,
                'errors': 1,
                'message': f'Import failed: {str(e)}'
            }
    
    def _import_places_list(self, places: List[Dict]) -> Dict:
        """Import a list of places to the database"""
        imported = 0
        skipped = 0
        errors = 0
        
        for i, place in enumerate(places):
            try:
                # Get detailed place information
                place_id = place.get('place_id')
                if not place_id:
                    logger.warning(f"Place {i+1} has no place_id, skipping")
                    skipped += 1
                    continue
                
                self._update_progress(i, len(places), 0, f"Processing place {i+1}/{len(places)}: {place.get('name', 'Unknown')}")
                
                # Check if we already have this place
                if Business.objects.filter(google_place_id=place_id).exists():
                    logger.info(f"Place {place.get('name')} already exists, skipping")
                    skipped += 1
                    continue
                
                # Get detailed information
                detailed_place = self.places_service.get_place_details(place_id)
                if not detailed_place:
                    logger.warning(f"Could not get details for place {place_id}")
                    errors += 1
                    continue
                
                # Convert to business data
                business_data = self.places_service.convert_place_to_business_data(detailed_place)
                
                # Create the business
                success = self._create_business_from_data(business_data)
                if success:
                    imported += 1
                    logger.info(f"Successfully imported: {business_data.get('name')}")
                else:
                    errors += 1
                
            except Exception as e:
                logger.error(f"Error processing place {i+1}: {e}")
                errors += 1
                continue
        
        return {
            'success': True,
            'imported': imported,
            'skipped': skipped,
            'errors': errors,
            'message': f'Import completed: {imported} imported, {skipped} skipped, {errors} errors'
        }
    
    def _create_business_from_data(self, business_data: Dict) -> bool:
        """Create a Business object from the converted data"""
        try:
            with transaction.atomic():
                # Get or create category
                category_name = business_data.pop('category_name', 'General Business')
                category, created = Category.objects.get_or_create(
                    name=category_name,
                    defaults={
                        'slug': category_name.lower().replace(' ', '-').replace('&', 'and'),
                        'description': f'Businesses in {category_name}',
                        'is_active': True,
                    }
                )
                
                # Remove Google-specific fields that aren't in Business model
                google_place_id = business_data.pop('google_place_id', '')
                google_rating = business_data.pop('google_rating', None)
                google_ratings_total = business_data.pop('google_ratings_total', None)
                
                # Create the business
                business = Business.objects.create(
                    owner=self.user,
                    category=category,
                    slug=self._generate_slug(business_data['name']),
                    imported_from_csv=False,  # This is from Google Places API
                    google_place_id=google_place_id,
                    google_import_date=timezone.now(),
                    is_active=True,
                    is_public=True,
                    is_verified=False,  # Will need manual verification
                    **business_data
                )
                
                logger.info(f"Created business: {business.name} (ID: {business.id})")
                return True
                
        except Exception as e:
            logger.error(f"Error creating business from data: {e}")
            logger.error(f"Business data: {business_data}")
            return False
    
    def _generate_slug(self, name: str) -> str:
        """Generate a unique slug for the business"""
        from django.utils.text import slugify
        
        base_slug = slugify(name)
        slug = base_slug
        counter = 1
        
        while Business.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        return slug
    
    def _update_progress(self, processed: int, total: int, errors: int, message: str):
        """Update import progress in cache"""
        if not self.progress_key:
            return
        
        percentage = (processed / total * 100) if total > 0 else 0
        
        progress_data = {
            'processed': processed,
            'total': total,
            'errors': errors,
            'percentage': round(percentage, 1),
            'message': message,
            'timestamp': timezone.now().isoformat(),
        }
        
        cache.set(self.progress_key, progress_data, timeout=3600)  # 1 hour cache
    
    def get_progress(self) -> Dict:
        """Get current import progress"""
        if not self.progress_key:
            return {'message': 'No import in progress'}
        
        return cache.get(self.progress_key, {'message': 'No progress data found'})