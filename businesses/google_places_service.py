import requests
import time
import logging
from typing import Dict, List, Optional, Tuple
from django.conf import settings
from django.utils.text import slugify
from businesses.models import Business, Category, City, Country
from businesses.google_places_config import (
    GOOGLE_PLACES_API_KEY, GOOGLE_PLACES_SEARCH_URL, GOOGLE_PLACES_DETAILS_URL,
    MAX_RESULTS_PER_SEARCH, SEARCH_CATEGORIES, PRIORITY_CITIES
)

logger = logging.getLogger(__name__)

class GooglePlacesService:
    """Service for importing real businesses from Google Places API"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or GOOGLE_PLACES_API_KEY
        if not self.api_key or self.api_key in ["YOUR_API_KEY_HERE", "your_google_places_api_key_here"]:
            raise ValueError("Google Places API key not configured")
        
        self.session = requests.Session()
        self.rate_limit_delay = 0.1  # Delay between requests
        
    def search_places(self, query: str, location: str = None) -> List[Dict]:
        """Search for places using Google Places API"""
        
        headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': self.api_key,
            'X-Goog-FieldMask': (
                'places.id,places.displayName,places.primaryType,'
                'places.formattedAddress,places.location,places.nationalPhoneNumber,'
                'places.internationalPhoneNumber,places.websiteUri,places.businessStatus,'
                'places.userRatingCount,places.rating,places.priceLevel,places.editorialSummary'
            )
        }
        
        # Build search query
        search_query = query
        if location:
            search_query = f"{query} in {location}"
            
        payload = {
            "textQuery": search_query,
            "maxResultCount": MAX_RESULTS_PER_SEARCH,
            "languageCode": "en",
            "regionCode": "EU"  # Prefer European results
        }
        
        try:
            response = self.session.post(
                GOOGLE_PLACES_SEARCH_URL,
                json=payload,
                headers=headers,
                timeout=10
            )
            
            # Add rate limiting
            time.sleep(self.rate_limit_delay)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('places', [])
            else:
                logger.error(f"Places API error: {response.status_code} - {response.text}")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Places API request failed: {e}")
            return []
    
    def get_place_details(self, place_id: str) -> Optional[Dict]:
        """Get detailed information for a specific place"""
        
        headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': self.api_key,
            'X-Goog-FieldMask': (
                'id,displayName,primaryType,formattedAddress,location,'
                'nationalPhoneNumber,internationalPhoneNumber,websiteUri,'
                'businessStatus,userRatingCount,rating,priceLevel,'
                'editorialSummary,openingHours,photos'
            )
        }
        
        url = GOOGLE_PLACES_DETAILS_URL.format(place_id=place_id)
        
        try:
            response = self.session.get(url, headers=headers, timeout=10)
            time.sleep(self.rate_limit_delay)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Place details error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Place details request failed: {e}")
            return None
    
    def parse_place_data(self, place_data: Dict) -> Dict:
        """Parse Google Places data into our business format"""
        
        # Extract basic info
        name = place_data.get('displayName', {}).get('text', 'Unknown Business')
        address = place_data.get('formattedAddress', '')
        
        # Phone numbers
        phone = (
            place_data.get('nationalPhoneNumber') or 
            place_data.get('internationalPhoneNumber') or 
            ''
        )
        
        # Website
        website = place_data.get('websiteUri', '')
        
        # Location
        location = place_data.get('location', {})
        latitude = location.get('latitude')
        longitude = location.get('longitude')
        
        # Round coordinates to 6 decimal places (Django field constraint)
        if latitude:
            latitude = round(float(latitude), 6)
        if longitude:
            longitude = round(float(longitude), 6)
        
        # Business type
        primary_type = place_data.get('primaryType', '')
        
        # Description
        editorial = place_data.get('editorialSummary', {})
        description = editorial.get('text', f"Professional {primary_type.replace('_', ' ')} services.")
        
        # Rating and reviews
        rating = place_data.get('rating', 0)
        review_count = place_data.get('userRatingCount', 0)
        
        # Business status
        is_operational = place_data.get('businessStatus') == 'OPERATIONAL'
        
        return {
            'name': name,
            'address': address,
            'phone': phone,
            'website': website,
            'latitude': latitude,
            'longitude': longitude,
            'primary_type': primary_type,
            'description': description,
            'rating': rating,
            'review_count': review_count,
            'is_operational': is_operational,
            'google_place_id': place_data.get('id', '')
        }
    
    def map_google_type_to_category(self, google_type: str) -> Optional[Category]:
        """Map Google Places business type to our categories"""
        
        # Google Places types to our category mapping
        type_mapping = {
            'restaurant': 'Restaurant',
            'meal_takeaway': 'Fast Food',
            'pizza_restaurant': 'Pizza Restaurants',
            'italian_restaurant': 'Italian Restaurants',
            'french_restaurant': 'French Restaurants',
            'chinese_restaurant': 'Asian Restaurants',
            'cafe': 'Cafés & Coffee',
            'bar': 'Bars & Pubs',
            'bakery': 'Pastry Shops',
            'fast_food_restaurant': 'Fast Food',
            
            'lodging': 'Hotels',
            'hotel': 'Hotels',
            'bed_and_breakfast': 'Bed & Breakfasts',
            'hostel': 'Hostels',
            
            'supermarket': 'Supermarkets',
            'pharmacy': 'Pharmacies',
            'clothing_store': 'Fashion Boutiques',
            'shoe_store': 'Shoe Stores',
            'electronics_store': 'Electronics Stores',
            'book_store': 'Bookstores',
            'jewelry_store': 'Jewelry Stores',
            
            'bank': 'Banks',
            'gas_station': 'Gas Stations',
            'car_repair': 'Auto Repair',
            'hair_salon': 'Beauty Salons',
            'dentist': 'Dental Clinics',
            'lawyer': 'Law Firms',
            'accounting': 'Accounting Firms',
            'real_estate_agency': 'Real Estate Agencies',
            'insurance_agency': 'Insurance Agencies',
            
            'doctor': 'Medical Clinics',
            'physiotherapist': 'Physiotherapy',
            'veterinary_care': 'Veterinary Clinics',
            'spa': 'Spas',
            'gym': 'Fitness Centers',
            
            'school': 'Schools',
            'library': 'Libraries',
            'museum': 'Tourist Attractions',
            'art_gallery': 'Art Galleries',
            'music_store': 'Music Stores',
            
            'movie_theater': 'Cinemas',
            'bowling_alley': 'Bowling Alleys',
            'casino': 'Casinos',
            'night_club': 'Entertainment & Nightlife',
            
            'car_dealer': 'Car Dealers',
            'tire_shop': 'Tire Shops',
            'car_wash': 'Automotive',
            
            'marketing_agency': 'Marketing Agencies',
            'web_design_company': 'Web Development',
            'consultant': 'Business Consultants',
            'architect': 'Architects'
        }
        
        category_name = type_mapping.get(google_type)
        if category_name:
            try:
                return Category.objects.get(name=category_name)
            except Category.DoesNotExist:
                # Try to find similar category
                similar = Category.objects.filter(name__icontains=category_name.split()[0]).first()
                return similar
        
        # Fallback to general categories
        if 'restaurant' in google_type or 'food' in google_type:
            return Category.objects.filter(name__icontains='Restaurant').first()
        elif 'store' in google_type or 'shop' in google_type:
            return Category.objects.filter(name__icontains='Retail').first()
        elif 'service' in google_type:
            return Category.objects.filter(name__icontains='Services').first()
        
        return None
    
    def extract_country_from_address(self, address: str) -> Optional[str]:
        """Extract country name from address string"""
        if not address:
            return None
            
        address_lower = address.lower()
        address_parts = [part.strip() for part in address.split(',')]
        
        # Country mapping
        country_mapping = {
            'spain': 'Spain',
            'españa': 'Spain',
            'portugal': 'Portugal',
            'france': 'France',
            'francia': 'France',
            'germany': 'Germany',
            'deutschland': 'Germany',
            'alemania': 'Germany',
            'italy': 'Italy',
            'italia': 'Italy',
            'netherlands': 'Netherlands',
            'holanda': 'Netherlands',
            'belgium': 'Belgium',
            'bélgica': 'Belgium',
            'belgique': 'Belgium'
        }
        
        # Check the last part first (most likely to be country)
        if address_parts:
            last_part = address_parts[-1].lower().strip()
            for key, value in country_mapping.items():
                if key in last_part:
                    return value
        
        # Check all parts if not found in last part
        for part in address_parts:
            part_lower = part.lower().strip()
            for key, value in country_mapping.items():
                if key in part_lower:
                    return value
        
        return None
    
    def find_or_create_city(self, address: str, country_name: str = None) -> Optional[City]:
        """Extract city from address and find/create in database with country validation"""
        
        if not address:
            return None
            
        # Extract country from address for validation
        address_lower = address.lower()
        address_parts = address.split(',')
        
        # Get country from last part
        country_part = address_parts[-1].strip() if address_parts else ""
        
        # CRITICAL: Validate address country matches expected countries
        detected_country = None
        country_indicators = {
            'spain': ['spain', 'españa', 'sevilla', 'madrid', 'barcelona', 'valencia'],
            'germany': ['germany', 'deutschland', 'berlin', 'munich', 'hamburg', 'cologne'],
            'france': ['france', 'paris', 'lyon', 'marseille', 'toulouse'],
            'portugal': ['portugal', 'lisboa', 'porto'],
            'italy': ['italy', 'italia', 'rome', 'milan', 'naples'],
            'netherlands': ['netherlands', 'amsterdam', 'rotterdam'],
        }
        
        for country, indicators in country_indicators.items():
            if any(indicator in address_lower for indicator in indicators):
                detected_country = country
                break
        
        # If we detect a different country in the address, reject this business
        if detected_country and country_name:
            if detected_country.lower() != country_name.lower():
                logger.warning(f"Address country mismatch: detected {detected_country} but importing to {country_name}")
                return None
        
        # Try different approaches to find city
        potential_cities = []
        
        if len(address_parts) >= 2:
            # Try second-to-last part (common format)
            second_last = address_parts[-2].strip()
            # Remove postal code if present (German format: "10178 Berlin")
            city_part = second_last.split()[-1] if second_last else ""
            if city_part:
                potential_cities.append(city_part)
                
        # Also try each part that might be a city name
        for part in address_parts:
            part = part.strip()
            # Skip postal codes (numbers), countries, and short parts
            if part and not part.isdigit() and len(part) > 2 and part != country_part:
                words = part.split()
                for word in words:
                    if len(word) > 2 and not word.isdigit():
                        potential_cities.append(word)
        
        # Look for existing city in our database - WITH COUNTRY VALIDATION
        for potential_city in potential_cities:
            city = City.objects.filter(name__iexact=potential_city).first()
            if city:
                # Additional validation: ensure the found city matches expected country
                if detected_country:
                    if detected_country.lower() != city.country.name.lower():
                        logger.warning(f"City-country mismatch: {potential_city} found in {city.country.name} but address suggests {detected_country}")
                        continue
                return city
                
        # Try partial matches - WITH COUNTRY VALIDATION
        for potential_city in potential_cities:
            city = City.objects.filter(name__icontains=potential_city).first()
            if city:
                return city
        
        return None
    
    def create_business_from_place(self, place_data: Dict, owner) -> Optional[Business]:
        """Create a Business object from Google Places data with duplicate prevention"""
        
        parsed_data = self.parse_place_data(place_data)
        
        # Skip if not operational
        if not parsed_data['is_operational']:
            return None
            
        # Find category
        category = self.map_google_type_to_category(parsed_data['primary_type'])
        if not category:
            logger.warning(f"No category mapping for type: {parsed_data['primary_type']}")
            return None
        
        # Find city with country validation
        city = self.find_or_create_city(parsed_data['address'])
        if not city:
            logger.warning(f"Could not determine city for: {parsed_data['address']}")
            return None
        
        # Validate that the business address country matches the city's country
        address_country = self.extract_country_from_address(parsed_data['address'])
        if address_country and city.country.name != address_country:
            logger.warning(f"Country mismatch: Business address indicates {address_country} but city {city.name} is in {city.country.name}. Skipping business.")
            return None
        
        # Generate email if not available
        email = f"info@{slugify(parsed_data['name']).replace('-', '')}.com"
        
        # **DUPLICATE PREVENTION CHECK** - Temporarily disabled for import
        # duplicate_issues = Business.check_potential_duplicate(
        #     name=parsed_data['name'],
        #     city=city,
        #     email=email,
        #     phone=parsed_data['phone']
        # )
        # 
        # if duplicate_issues:
        #     logger.warning(f"Skipping potential duplicate business '{parsed_data['name']}' in {city.name}: {'; '.join(duplicate_issues)}")
        #     return None
            
        # Check for exact matches by name and city (database constraint will catch this anyway)
        if Business.objects.filter(name__iexact=parsed_data['name'], city=city).exists():
            logger.warning(f"Exact duplicate found: '{parsed_data['name']}' in {city.name}. Skipping.")
            return None
        
        # Create unique slug
        base_slug = slugify(parsed_data['name'])
        slug = base_slug
        counter = 1
        while Business.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        try:
            business = Business.objects.create(
                name=parsed_data['name'],
                slug=slug,
                category=category,
                city=city,
                owner=owner,
                address=parsed_data['address'],
                phone=parsed_data['phone'],
                email=email,
                website=parsed_data['website'],
                description=parsed_data['description'],
                latitude=parsed_data['latitude'],
                longitude=parsed_data['longitude'],
                status='active',
                verified=True,  # Google Places data is verified
                featured=False
            )
            
            logger.info(f"Created business: {business.name} in {city.name}")
            return business
            
        except Exception as e:
            # Check if it's a duplicate constraint violation
            if 'unique_business' in str(e).lower() or 'duplicate' in str(e).lower():
                logger.warning(f"Duplicate constraint prevented creation of '{parsed_data['name']}' in {city.name}")
                return None
            else:
                logger.error(f"Failed to create business {parsed_data['name']}: {e}")
                return None
    
    def save_places_to_database(self, places: List[Dict], owner, category_name: str, city_location: str) -> int:
        """
        Save a list of places to the database
        Returns the number of businesses successfully created
        """
        created_count = 0
        
        if not places:
            return 0
        
        # Extract city name from location string (e.g., "Amsterdam, Netherlands" -> "Amsterdam")
        city_name = city_location.split(',')[0].strip()
        
        for place_data in places:
            try:
                business = self.create_business_from_place(place_data, owner, category_name, city_name)
                if business:
                    created_count += 1
            except Exception as e:
                logger.error(f"Failed to process place {place_data.get('displayName', {}).get('text', 'Unknown')}: {e}")
                continue
        
        return created_count