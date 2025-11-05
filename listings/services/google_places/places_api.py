"""
Google Places API Integration Service

This service handles fetching business data from Google Places API
and converting it to our Django Business model format.
"""

import googlemaps
import time
from typing import List, Dict, Optional
from django.conf import settings
from django.core.cache import cache
from listings.models import Business, Category
from accounts.models import User
import logging

logger = logging.getLogger(__name__)


class GooglePlacesService:
    """Service for importing businesses from Google Places API"""
    
    def __init__(self):
        """Initialize the Google Maps client"""
        self.api_key = settings.GOOGLE_PLACES_API_KEY
        if not self.api_key:
            raise ValueError("Google Places API key not configured. Set GOOGLE_PLACES_API_KEY environment variable.")
        
        self.client = googlemaps.Client(key=self.api_key)
        self.max_results = getattr(settings, 'GOOGLE_PLACES_MAX_RESULTS', 20)
        self.radius = getattr(settings, 'GOOGLE_PLACES_RADIUS', 5000)
        self.rate_limit = getattr(settings, 'GOOGLE_PLACES_RATE_LIMIT', 0.1)
    
    def search_places_by_query(self, query: str, location: str = None, region: str = None) -> List[Dict]:
        """
        Search for places using a text query
        
        Args:
            query: Search query (e.g., "restaurants in Paris")
            location: Optional location bias (e.g., "Paris, France")
            region: Optional region code (e.g., "fr")
            
        Returns:
            List of place dictionaries from Google Places API
        """
        try:
            logger.info(f"Searching Google Places for: {query}")
            
            # Build search parameters
            search_params = {
                'query': query,
            }
            
            if location:
                # Get coordinates for location bias
                geocode_result = self.client.geocode(location)
                if geocode_result:
                    lat = geocode_result[0]['geometry']['location']['lat']
                    lng = geocode_result[0]['geometry']['location']['lng']
                    search_params['location'] = (lat, lng)
                    search_params['radius'] = self.radius
            
            if region:
                search_params['region'] = region
            
            # Execute search
            places_result = self.client.places(**search_params)
            
            # Rate limiting
            time.sleep(self.rate_limit)
            
            return places_result.get('results', [])
            
        except Exception as e:
            logger.error(f"Error searching Google Places: {e}")
            return []
    
    def search_places_nearby(self, location: str, place_type: str = None) -> List[Dict]:
        """
        Search for places near a specific location
        
        Args:
            location: Location to search near (e.g., "Paris, France")
            place_type: Optional place type filter (e.g., "restaurant", "store")
            
        Returns:
            List of place dictionaries from Google Places API
        """
        try:
            logger.info(f"Searching nearby places in: {location}")
            
            # Get coordinates for the location
            geocode_result = self.client.geocode(location)
            if not geocode_result:
                logger.error(f"Could not geocode location: {location}")
                return []
            
            lat = geocode_result[0]['geometry']['location']['lat']
            lng = geocode_result[0]['geometry']['location']['lng']
            
            # Build search parameters
            search_params = {
                'location': (lat, lng),
                'radius': self.radius,
            }
            
            if place_type:
                search_params['type'] = place_type
            
            # Execute nearby search
            places_result = self.client.places_nearby(**search_params)
            
            # Rate limiting
            time.sleep(self.rate_limit)
            
            return places_result.get('results', [])
            
        except Exception as e:
            logger.error(f"Error searching nearby places: {e}")
            return []
    
    def get_place_details(self, place_id: str) -> Optional[Dict]:
        """
        Get detailed information for a specific place
        
        Args:
            place_id: Google Places ID
            
        Returns:
            Detailed place information or None if error
        """
        try:
            # Define fields to retrieve
            fields = [
                'place_id', 'name', 'formatted_address', 'geometry',
                'formatted_phone_number', 'website', 'rating',
                'user_ratings_total', 'type', 'opening_hours',
                'business_status', 'price_level'
            ]
            
            place_details = self.client.place(
                place_id=place_id,
                fields=fields
            )
            
            # Rate limiting
            time.sleep(self.rate_limit)
            
            return place_details.get('result', {})
            
        except Exception as e:
            logger.error(f"Error getting place details for {place_id}: {e}")
            return None
    
    def convert_place_to_business_data(self, place_data: Dict) -> Dict:
        """
        Convert Google Places data to our Business model format
        
        Args:
            place_data: Place data from Google Places API
            
        Returns:
            Dictionary formatted for Business model creation
        """
        # Extract basic information
        name = place_data.get('name', '')
        address = place_data.get('formatted_address', '')
        
        # Parse address components
        address_parts = address.split(', ') if address else []
        city = ''
        country = ''
        postal_code = ''
        
        if len(address_parts) >= 2:
            city = address_parts[-2]
            country = address_parts[-1]
        
        # Extract coordinates
        geometry = place_data.get('geometry', {})
        location = geometry.get('location', {})
        latitude = location.get('lat')
        longitude = location.get('lng')
        
        # Extract contact info
        phone = place_data.get('formatted_phone_number', '')
        website = place_data.get('website', '')
        
        # Map Google Place types to our categories
        place_types = place_data.get('type', place_data.get('types', []))
        category_name = self._map_google_type_to_category(place_types)
        
        # Extract opening hours
        opening_hours = place_data.get('opening_hours', {})
        weekday_text = opening_hours.get('weekday_text', [])
        
        # Parse weekday hours
        hours_data = self._parse_opening_hours(weekday_text)
        
        # Build business data
        business_data = {
            'name': name,
            'description': f"Business imported from Google Places. Rating: {place_data.get('rating', 'N/A')}",
            'email': '',  # Google Places doesn't provide email
            'phone': phone,
            'website': website,
            'address': address,
            'city': city,
            'country': country,
            'postal_code': postal_code,
            'latitude': latitude,
            'longitude': longitude,
            'category_name': category_name,
            'google_place_id': place_data.get('place_id', ''),
            'google_rating': place_data.get('rating'),
            'google_ratings_total': place_data.get('user_ratings_total'),
            **hours_data
        }
        
        return business_data
    
    def _map_google_type_to_category(self, place_types: List[str]) -> str:
        """Map Google Place types to our category names"""
        
        # Define mapping from Google types to our categories
        type_mapping = {
            'restaurant': 'Restaurants',
            'food': 'Food & Beverages',
            'meal_takeaway': 'Restaurants',
            'meal_delivery': 'Restaurants',
            'cafe': 'Cafes',
            'bar': 'Bars & Pubs',
            'lodging': 'Hotels',
            'tourist_attraction': 'Tourism',
            'shopping_mall': 'Shopping Centers',
            'store': 'Retail Stores',
            'clothing_store': 'Fashion & Clothing',
            'electronics_store': 'Electronics',
            'book_store': 'Books & Media',
            'pharmacy': 'Pharmacy',
            'hospital': 'Healthcare',
            'doctor': 'Healthcare',
            'dentist': 'Healthcare',
            'gym': 'Fitness & Sports',
            'beauty_salon': 'Beauty & Wellness',
            'hair_care': 'Beauty & Wellness',
            'spa': 'Beauty & Wellness',
            'car_dealer': 'Automotive',
            'car_repair': 'Auto Repair',
            'gas_station': 'Gas Stations',
            'bank': 'Financial Services',
            'atm': 'Financial Services',
            'real_estate_agency': 'Real Estate',
            'lawyer': 'Legal Services',
            'accounting': 'Accounting Firms',
            'school': 'Education',
            'university': 'Education',
            'church': 'Religious Organizations',
            'art_gallery': 'Art Galleries',
            'museum': 'Museums',
            'night_club': 'Entertainment',
            'movie_theater': 'Entertainment',
        }
        
        # Find the first matching type
        for place_type in place_types:
            if place_type in type_mapping:
                return type_mapping[place_type]
        
        # Default category if no match found
        return 'General Business'
    
    def _parse_opening_hours(self, weekday_text: List[str]) -> Dict:
        """Parse Google Places opening hours format to our model fields"""
        hours_data = {
            'monday_hours': '',
            'tuesday_hours': '',
            'wednesday_hours': '',
            'thursday_hours': '',
            'friday_hours': '',
            'saturday_hours': '',
            'sunday_hours': '',
        }
        
        day_mapping = {
            'Monday': 'monday_hours',
            'Tuesday': 'tuesday_hours',
            'Wednesday': 'wednesday_hours',
            'Thursday': 'thursday_hours',
            'Friday': 'friday_hours',
            'Saturday': 'saturday_hours',
            'Sunday': 'sunday_hours',
        }
        
        for day_text in weekday_text:
            for day_name, field_name in day_mapping.items():
                if day_text.startswith(day_name):
                    # Extract hours part after day name
                    hours_part = day_text.replace(f"{day_name}: ", "")
                    hours_data[field_name] = hours_part
                    break
        
        return hours_data