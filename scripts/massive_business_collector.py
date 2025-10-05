"""
Massive EU Business Data Collector
Target: 60 businesses per city × 820 cities = ~49,200 businesses
100% Legal data collection from multiple sources
"""

import os
import django
import requests
import json
import time
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listacrosseu.settings')
django.setup()

from businesses.models import Country, City, Category, Business


class MassiveBusinessCollector:
    """Collect 49,200+ businesses across EU legally"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ListAcross.eu Business Directory (contact@listacross.eu)'
        })
        self.businesses_added = 0
        self.businesses_skipped = 0
        self.target_per_city = 60
        
        # Rate limiting
        self.request_delay = 1  # 1 second between requests
        self.last_request = 0
    
    def rate_limit(self):
        """Implement rate limiting"""
        current_time = time.time()
        if current_time - self.last_request < self.request_delay:
            time.sleep(self.request_delay - (current_time - self.last_request))
        self.last_request = time.time()
    
    def collect_from_openstreetmap(self, city, category_mapping):
        """Collect businesses from OpenStreetMap (100% legal)"""
        
        if not city.latitude or not city.longitude:
            return []
        
        businesses = []
        
        # Overpass API query for businesses near city
        overpass_url = "http://overpass-api.de/api/interpreter"
        
        # Search radius based on city population
        radius = min(max(1000, city.population // 100), 10000)  # 1-10km radius
        
        # OSM queries for different business types
        queries = [
            f'[amenity~"restaurant|cafe|bar|pub"]',
            f'[shop]',
            f'[tourism~"hotel|hostel|guest_house|attraction"]',
            f'[amenity~"bank|pharmacy|hospital|dentist"]',
            f'[office]',
            f'[craft]'
        ]
        
        for query in queries:
            try:
                self.rate_limit()
                
                overpass_query = f"""
                [out:json][timeout:25];
                (
                  node{query}(around:{radius},{city.latitude},{city.longitude});
                  way{query}(around:{radius},{city.latitude},{city.longitude});
                  relation{query}(around:{radius},{city.latitude},{city.longitude});
                );
                out body;
                """
                
                response = self.session.post(
                    overpass_url,
                    data={'data': overpass_query},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    elements = data.get('elements', [])
                    
                    for element in elements[:20]:  # Limit per query
                        business_data = self.parse_osm_element(element, city)
                        if business_data:
                            businesses.append(business_data)
                            
                else:
                    print(f"⚠️ OSM API error: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ OSM query error: {e}")
                continue
        
        return businesses[:self.target_per_city]  # Limit to target
    
    def parse_osm_element(self, element, city):
        """Parse OSM element into business data"""
        
        tags = element.get('tags', {})
        name = tags.get('name', '').strip()
        
        if not name or len(name) < 2:
            return None
        
        # Get coordinates
        lat = element.get('lat')
        lon = element.get('lon')
        
        if not lat or not lon:
            # For ways/relations, use center point if available
            if 'center' in element:
                lat = element['center'].get('lat')
                lon = element['center'].get('lon')
        
        if not lat or not lon:
            return None
        
        # Determine category
        category = self.determine_category(tags)
        if not category:
            return None
        
        # Build business data
        business_data = {
            'name': name,
            'city': city,
            'category': category,
            'latitude': Decimal(str(lat)),
            'longitude': Decimal(str(lon)),
            'address': self.build_address(tags, city),
            'phone_number': tags.get('phone', ''),
            'website': tags.get('website', ''),
            'description': self.build_description(tags, category),
            'verified': True,
            'verification_method': 'openstreetmap',
            'source_data': json.dumps(tags)
        }
        
        return business_data
    
    def determine_category(self, tags):
        """Determine business category from OSM tags"""
        
        # Category mapping
        category_mapping = {
            # Food & Drink
            'restaurant': 'Restaurants',
            'cafe': 'Cafes & Coffee Shops', 
            'bar': 'Bars & Pubs',
            'pub': 'Bars & Pubs',
            'fast_food': 'Fast Food Chains',
            'bakery': 'Bakeries & Patisseries',
            'ice_cream': 'Ice Cream Parlors',
            
            # Shopping
            'supermarket': 'Supermarkets',
            'convenience': 'Supermarkets',
            'clothes': 'Fashion & Clothing',
            'shoes': 'Shoes & Accessories',
            'electronics': 'Electronics & Technology',
            'books': 'Books & Stationery',
            'pharmacy': 'Pharmacies',
            'optician': 'Optical Services',
            
            # Services
            'bank': 'Banks & Financial Services',
            'hospital': 'Hospitals',
            'dentist': 'Dental Clinics',
            'hairdresser': 'Hair Salons',
            'beauty': 'Beauty Salons',
            
            # Tourism
            'hotel': 'Hotels & Resorts',
            'hostel': 'Hostels',
            'guest_house': 'Bed & Breakfasts',
            'attraction': 'Tourist Attractions',
            'museum': 'Museums & Galleries',
            
            # Transport
            'fuel': 'Gas Stations',
            'car_rental': 'Car Rental Services',
            'taxi': 'Taxi Services',
        }
        
        # Check amenity first
        amenity = tags.get('amenity', '')
        if amenity in category_mapping:
            category_name = category_mapping[amenity]
            try:
                return Category.objects.get(name=category_name)
            except Category.DoesNotExist:
                pass
        
        # Check shop type
        shop = tags.get('shop', '')
        if shop in category_mapping:
            category_name = category_mapping[shop]
            try:
                return Category.objects.get(name=category_name)
            except Category.DoesNotExist:
                pass
        
        # Check tourism
        tourism = tags.get('tourism', '')
        if tourism in category_mapping:
            category_name = category_mapping[tourism]
            try:
                return Category.objects.get(name=category_name)
            except Category.DoesNotExist:
                pass
        
        # Default fallback
        try:
            return Category.objects.filter(parent__isnull=False).first()
        except:
            return None
    
    def build_address(self, tags, city):
        """Build address from OSM tags"""
        
        address_parts = []
        
        # House number and street
        if tags.get('addr:housenumber') and tags.get('addr:street'):
            address_parts.append(f"{tags['addr:street']} {tags['addr:housenumber']}")
        elif tags.get('addr:street'):
            address_parts.append(tags['addr:street'])
        
        # Postal code
        if tags.get('addr:postcode'):
            address_parts.append(tags['addr:postcode'])
        
        # City name
        address_parts.append(city.name)
        
        return ', '.join(address_parts) if address_parts else f"{city.name}, {city.country.name}"
    
    def build_description(self, tags, category):
        """Build business description from OSM tags"""
        
        descriptions = []
        
        # Add category-specific description
        descriptions.append(f"A {category.name.lower().rstrip('s')} located in {tags.get('addr:city', 'the area')}.")
        
        # Add cuisine info for restaurants
        if tags.get('cuisine'):
            descriptions.append(f"Specializes in {tags['cuisine']} cuisine.")
        
        # Add opening hours if available
        if tags.get('opening_hours'):
            descriptions.append(f"Opening hours: {tags['opening_hours']}.")
        
        # Add wheelchair accessibility
        if tags.get('wheelchair') == 'yes':
            descriptions.append("Wheelchair accessible.")
        
        # Add WiFi info
        if tags.get('internet_access') == 'wlan':
            descriptions.append("Free WiFi available.")
        
        return ' '.join(descriptions)
    
    def add_business(self, business_data):
        """Add business to database"""
        
        # Check if business already exists
        existing = Business.objects.filter(
            name=business_data['name'],
            city=business_data['city']
        ).first()
        
        if existing:
            self.businesses_skipped += 1
            return False
        
        try:
            business = Business.objects.create(**business_data)
            self.businesses_added += 1
            return True
            
        except Exception as e:
            print(f"❌ Error adding business '{business_data['name']}': {e}")
            return False
    
    def collect_for_city(self, city):
        """Collect businesses for a specific city"""
        
        current_count = Business.objects.filter(city=city).count()
        
        if current_count >= self.target_per_city:
            print(f"✅ {city.name} already has {current_count} businesses (target: {self.target_per_city})")
            return
        
        needed = self.target_per_city - current_count
        print(f"🏙️ Collecting businesses for {city.name}, {city.country.name} (need {needed} more)")
        
        # Collect from OpenStreetMap
        businesses = self.collect_from_openstreetmap(city, {})
        
        added_this_city = 0
        for business_data in businesses:
            if self.add_business(business_data):
                added_this_city += 1
                print(f"  ✅ Added: {business_data['name']}")
                
                if added_this_city >= needed:
                    break
        
        print(f"📊 {city.name}: Added {added_this_city} businesses")
    
    def run_massive_collection(self):
        """Run massive business collection across EU"""
        
        print("🏢 STARTING MASSIVE EU BUSINESS COLLECTION")
        print("=" * 60)
        print(f"🎯 Target: {self.target_per_city} businesses per city")
        
        initial_count = Business.objects.count()
        cities = City.objects.select_related('country').filter(
            latitude__isnull=False,
            longitude__isnull=False,
            population__gte=5000
        ).order_by('-population')
        
        total_cities = cities.count()
        target_businesses = total_cities * self.target_per_city
        
        print(f"📊 Processing {total_cities} cities")
        print(f"🎯 Target total businesses: {target_businesses:,}")
        print(f"📊 Current businesses: {initial_count}")
        
        # Process cities
        for i, city in enumerate(cities, 1):
            print(f"\n[{i}/{total_cities}] Processing {city.name}, {city.country.name}")
            
            try:
                self.collect_for_city(city)
            except Exception as e:
                print(f"❌ Error processing {city.name}: {e}")
                continue
            
            # Progress update every 50 cities
            if i % 50 == 0:
                current_total = Business.objects.count()
                progress = (i / total_cities) * 100
                print(f"\n📈 PROGRESS UPDATE: {progress:.1f}% complete")
                print(f"📊 Total businesses now: {current_total:,}")
                print(f"✅ Added in this session: {self.businesses_added}")
                print("-" * 40)
        
        # Final statistics
        final_count = Business.objects.count()
        
        print("\n" + "=" * 60)
        print("🎉 MASSIVE BUSINESS COLLECTION COMPLETED!")
        print(f"📊 Initial businesses: {initial_count:,}")
        print(f"📊 Final businesses: {final_count:,}")
        print(f"✅ Businesses added: {self.businesses_added:,}")
        print(f"⏭️ Businesses skipped: {self.businesses_skipped:,}")
        print(f"📈 Total increase: {final_count - initial_count:,}")
        print(f"🎯 Target achievement: {(final_count/target_businesses)*100:.1f}%")
        
        # Show businesses per country
        print("\n🏛️ BUSINESSES PER COUNTRY:")
        for country in Country.objects.all():
            count = Business.objects.filter(city__country=country).count()
            cities_count = City.objects.filter(country=country).count()
            avg_per_city = count / cities_count if cities_count > 0 else 0
            print(f"  {country.name}: {count:,} businesses ({avg_per_city:.1f} per city)")


if __name__ == "__main__":
    collector = MassiveBusinessCollector()
    collector.run_massive_collection()