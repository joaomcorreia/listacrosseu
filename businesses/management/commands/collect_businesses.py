from django.core.management.base import BaseCommand
from businesses.models import Country, City, Category, Business
import requests
import time
import json
import random
from decimal import Decimal


class Command(BaseCommand):
    help = 'Collect businesses from OpenStreetMap for all EU cities'
    
    def __init__(self):
        super().__init__()
        self.added_businesses = 0
        self.skipped_businesses = 0
        self.errors = 0
        self.processed_cities = 0
        
        # OSM to category mapping
        self.osm_category_mapping = {
            'restaurant': 'Fine Dining Restaurants',
            'fast_food': 'Fast Food Restaurants',
            'cafe': 'Coffee Shops',
            'pub': 'Pubs',
            'bar': 'Cocktail Bars',
            'hotel': 'Business Hotels',
            'pharmacy': 'Pharmacies',
            'bank': 'Banks',
            'hospital': 'General Hospitals',
            'doctors': 'Private Clinics',
            'dentist': 'Dental Clinics',
            'hairdresser': 'Hair Salons',
            'beauty': 'Beauty Salons',
            'shop': 'Department Stores',
            'supermarket': 'Department Stores',
            'clothes': 'Clothing Stores',
            'shoes': 'Shoe Stores',
            'bakery': 'Bakeries',
            'fuel': 'Gas Stations',
            'car_repair': 'Auto Repair Shops',
            'cinema': 'Movie Theaters',
            'theatre': 'Theaters',
            'museum': 'Museums',
            'university': 'Universities',
            'school': 'Universities',
            'fitness_centre': 'Fitness Centers',
            'gym': 'Fitness Centers',
            'nightclub': 'Nightclubs',
            'casino': 'Casinos',
            'atm': 'ATMs',
            'car_wash': 'Car Wash',
            'taxi': 'Taxi Services',
        }
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--cities',
            type=int,
            default=50,
            help='Number of cities to process (default: 50)'
        )
        parser.add_argument(
            '--businesses-per-city',
            type=int,
            default=60,
            help='Target businesses per city (default: 60)'
        )
    
    def get_osm_businesses(self, city_name, country_name, latitude, longitude, limit=60):
        """Get businesses from OpenStreetMap using Overpass API"""
        
        # Overpass API query for various business types
        overpass_query = f"""
        [out:json][timeout:25];
        (
          node["amenity"~"^(restaurant|fast_food|cafe|pub|bar|hotel|pharmacy|bank|hospital|doctors|dentist|fuel|cinema|theatre|museum|university|school|fitness_centre|gym|nightclub|casino|atm|car_wash|taxi)$"](around:5000,{latitude},{longitude});
          node["shop"~"^(supermarket|clothes|shoes|bakery|hairdresser|beauty|convenience|mall|department_store|electronics|books|sports|jewelry|furniture|florist|hardware)$"](around:5000,{latitude},{longitude});
          node["tourism"~"^(hotel|hostel|guest_house|attraction|museum|gallery)$"](around:5000,{latitude},{longitude});
          node["office"~"^(lawyer|accountant|insurance|real_estate|employment_agency|it|architect|engineer)$"](around:5000,{latitude},{longitude});
        );
        out center meta;
        """
        
        overpass_url = "http://overpass-api.de/api/interpreter"
        
        try:
            response = requests.post(
                overpass_url,
                data=overpass_query,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                businesses = []
                
                for element in data.get('elements', []):
                    if len(businesses) >= limit:
                        break
                        
                    tags = element.get('tags', {})
                    name = tags.get('name', '')
                    
                    if not name:
                        continue
                    
                    # Determine business type
                    business_type = None
                    for key in ['amenity', 'shop', 'tourism', 'office']:
                        if key in tags:
                            business_type = tags[key]
                            break
                    
                    if not business_type:
                        continue
                    
                    # Get coordinates
                    if 'lat' in element and 'lon' in element:
                        lat = element['lat']
                        lon = element['lon']
                    elif 'center' in element:
                        lat = element['center']['lat']
                        lon = element['center']['lon']
                    else:
                        continue
                    
                    # Get address info
                    address = self.build_address(tags)
                    phone = tags.get('phone', '')
                    website = tags.get('website', '')
                    
                    businesses.append({
                        'name': name,
                        'type': business_type,
                        'latitude': lat,
                        'longitude': lon,
                        'address': address,
                        'phone': phone,
                        'website': website
                    })
                
                return businesses
                
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ API Error {response.status_code} for {city_name}')
                )
                return []
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Request failed for {city_name}: {str(e)}')
            )
            return []
    
    def build_address(self, tags):
        """Build address from OSM tags"""
        address_parts = []
        
        if 'addr:housenumber' in tags:
            address_parts.append(tags['addr:housenumber'])
        if 'addr:street' in tags:
            address_parts.append(tags['addr:street'])
        if 'addr:city' in tags:
            address_parts.append(tags['addr:city'])
        if 'addr:postcode' in tags:
            address_parts.append(tags['addr:postcode'])
            
        return ', '.join(address_parts) if address_parts else ''
    
    def get_category_for_business(self, business_type):
        """Map OSM business type to our category"""
        # Direct mapping
        if business_type in self.osm_category_mapping:
            category_name = self.osm_category_mapping[business_type]
            try:
                return Category.objects.get(name=category_name)
            except Category.DoesNotExist:
                pass
        
        # Fallback to first available category
        try:
            return Category.objects.first()
        except:
            return None
    
    def handle(self, *args, **options):
        max_cities = options['cities']
        businesses_per_city = options['businesses_per_city']
        
        self.stdout.write(
            self.style.SUCCESS(
                f'🚀 Starting Business Collection from OpenStreetMap'
            )
        )
        self.stdout.write(f'📍 Processing {max_cities} cities')
        self.stdout.write(f'🏢 Target: {businesses_per_city} businesses per city')
        self.stdout.write(f'🎯 Total target: {max_cities * businesses_per_city:,} businesses')
        self.stdout.write('='*60)
        
        # Get cities to process (prioritize larger cities)
        cities = City.objects.filter(
            latitude__isnull=False,
            longitude__isnull=False
        ).order_by('-population')[:max_cities]
        
        if not cities.exists():
            self.stdout.write(
                self.style.ERROR('❌ No cities with coordinates found!')
            )
            return
        
        for city in cities:
            self.processed_cities += 1
            
            self.stdout.write(
                f'\n🏙️  Processing {city.name}, {city.country.name} '
                f'({self.processed_cities}/{max_cities})'
            )
            
            # Check if city already has enough businesses
            existing_count = Business.objects.filter(city=city).count()
            if existing_count >= businesses_per_city:
                self.stdout.write(
                    f'⏭️  Skipped: {city.name} already has {existing_count} businesses'
                )
                continue
            
            # Get businesses from OpenStreetMap
            businesses_data = self.get_osm_businesses(
                city.name,
                city.country.name,
                float(city.latitude),
                float(city.longitude),
                businesses_per_city
            )
            
            if not businesses_data:
                self.stdout.write(f'❌ No businesses found for {city.name}')
                self.errors += 1
                continue
            
            # Process each business
            city_added = 0
            for business_data in businesses_data:
                try:
                    # Check if business already exists
                    if Business.objects.filter(
                        name=business_data['name'],
                        city=city
                    ).exists():
                        self.skipped_businesses += 1
                        continue
                    
                    # Get category
                    category = self.get_category_for_business(business_data['type'])
                    if not category:
                        continue
                    
                    # Generate safe slug
                    import re
                    base_slug = re.sub(r'[^a-zA-Z0-9\-]', '', business_data['name'].lower().replace(' ', '-').replace('&', 'and'))
                    base_slug = base_slug[:40]  # Limit length
                    city_slug = re.sub(r'[^a-zA-Z0-9\-]', '', city.name.lower().replace(' ', '-'))
                    slug = f"{base_slug}-{city_slug}-{self.added_businesses}"
                    
                    # Generate safe email
                    safe_name = re.sub(r'[^a-zA-Z0-9]', '', business_data['name'].lower())[:20]
                    email = f"info.{safe_name}@example.com"
                    
                    # Create business - need to add required fields
                    business = Business.objects.create(
                        name=business_data['name'][:200],  # Limit to field max length
                        slug=slug,
                        description=f"{business_data['name']} - {category.name} in {city.name}, {city.country.name}",
                        email=email,
                        category=category,
                        city=city,
                        address=business_data['address'][:500] if business_data['address'] else f"{city.name}, {city.country.name}",
                        phone=business_data['phone'][:20],
                        website=business_data['website'][:200] if business_data['website'] else '',
                        latitude=Decimal(str(business_data['latitude'])),
                        longitude=Decimal(str(business_data['longitude'])),
                        owner_id=2  # Admin user
                    )
                    
                    self.added_businesses += 1
                    city_added += 1
                    
                    if city_added % 10 == 0:
                        self.stdout.write(f'  ✅ Added {city_added} businesses to {city.name}')
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'❌ Error adding {business_data["name"]}: {str(e)}'
                        )
                    )
                    self.errors += 1
                    continue
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ {city.name}: Added {city_added} businesses')
            )
            
            # Rate limiting - respect OpenStreetMap's usage policy
            time.sleep(1)
        
        # Final statistics
        self.stdout.write('\n' + '='*60)
        self.stdout.write(
            self.style.SUCCESS('🎉 Business Collection Complete!')
        )
        self.stdout.write(f'🏙️  Cities processed: {self.processed_cities}')
        self.stdout.write(f'✅ Businesses added: {self.added_businesses}')
        self.stdout.write(f'⏭️  Businesses skipped: {self.skipped_businesses}')
        self.stdout.write(f'❌ Errors: {self.errors}')
        
        total_businesses = Business.objects.count()
        self.stdout.write(f'🏢 Total businesses in database: {total_businesses:,}')
        
        if total_businesses >= 1000:
            self.stdout.write(
                self.style.SUCCESS('🎯 Milestone achieved: 1,000+ businesses!')
            )
        
        # Show top cities by business count
        self.stdout.write('\n📊 Top 10 Cities by Business Count:')
        from django.db.models import Count
        top_cities = City.objects.annotate(
            business_count=Count('businesses')
        ).order_by('-business_count')[:10]
        
        for i, city in enumerate(top_cities, 1):
            self.stdout.write(
                f'{i:2d}. {city.name}, {city.country.name}: '
                f'{city.business_count} businesses'
            )