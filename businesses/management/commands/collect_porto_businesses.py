from django.core.management.base import BaseCommand
from businesses.models import City, Business, Category
import requests
import time
from decimal import Decimal
import re


class Command(BaseCommand):
    help = 'Collect businesses specifically for Porto, Portugal'
    
    def handle(self, *args, **options):
        try:
            porto = City.objects.get(name='Porto', country__code='PT')
            self.stdout.write(f'Collecting businesses for {porto.name}, {porto.country.name}')
            
            # Get businesses from OpenStreetMap
            businesses_data = self.get_osm_businesses_for_porto(
                float(porto.latitude), 
                float(porto.longitude)
            )
            
            if not businesses_data:
                self.stdout.write('No businesses found')
                return
            
            added = 0
            for business_data in businesses_data:
                try:
                    # Check if business already exists
                    if Business.objects.filter(name=business_data['name'], city=porto).exists():
                        continue
                    
                    # Get or create category
                    category = self.get_category_for_business(business_data['type'])
                    
                    # Generate slug
                    base_slug = re.sub(r'[^a-zA-Z0-9\-]', '', business_data['name'].lower().replace(' ', '-'))[:40]
                    slug = f"{base_slug}-{porto.slug}"
                    counter = 1
                    while Business.objects.filter(slug=slug).exists():
                        slug = f"{base_slug}-{porto.slug}-{counter}"
                        counter += 1
                    
                    # Create business
                    business = Business.objects.create(
                        name=business_data['name'][:200],
                        slug=slug,
                        description=f"{business_data['name']} - {category.name} in Porto, Portugal. {business_data.get('description', '')}",
                        email=f"info.{re.sub(r'[^a-zA-Z0-9]', '', business_data['name'].lower())[:20]}@example.com",
                        category=category,
                        city=porto,
                        address=business_data.get('address', 'Porto, Portugal'),
                        phone=business_data.get('phone', ''),
                        website=business_data.get('website', ''),
                        latitude=Decimal(str(business_data['latitude'])),
                        longitude=Decimal(str(business_data['longitude'])),
                        owner_id=2,  # Admin user
                        verified=True,
                        status='active'
                    )
                    
                    added += 1
                    self.stdout.write(f'✅ Added: {business_data["name"]}')
                    
                except Exception as e:
                    self.stdout.write(f'❌ Error: {business_data["name"]} - {str(e)}')
            
            self.stdout.write(f'🎉 Added {added} businesses to Porto!')
            
        except Exception as e:
            self.stdout.write(f'❌ Error: {str(e)}')
    
    def get_osm_businesses_for_porto(self, lat, lng):
        """Get businesses from OpenStreetMap for Porto"""
        
        overpass_query = f"""
        [out:json][timeout:25];
        (
          node["amenity"~"^(restaurant|fast_food|cafe|pub|bar|hotel|pharmacy|bank|hospital|doctors|dentist|fuel|cinema|theatre|museum|university|school|fitness_centre|gym|nightclub|casino|atm|car_wash|taxi)$"](around:8000,{lat},{lng});
          node["shop"~"^(supermarket|clothes|shoes|bakery|hairdresser|beauty|convenience|mall|department_store|electronics|books|sports|jewelry|furniture|florist|hardware)$"](around:8000,{lat},{lng});
          node["tourism"~"^(hotel|hostel|guest_house|attraction|museum|gallery)$"](around:8000,{lat},{lng});
          node["office"~"^(lawyer|accountant|insurance|real_estate|employment_agency|it|architect|engineer)$"](around:8000,{lat},{lng});
        );
        out center meta;
        """
        
        try:
            response = requests.post(
                "http://overpass-api.de/api/interpreter",
                data=overpass_query,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                businesses = []
                
                for element in data.get('elements', []):
                    if len(businesses) >= 50:  # Limit for testing
                        break
                        
                    tags = element.get('tags', {})
                    name = tags.get('name', '')
                    
                    if not name or len(name) < 2:
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
                        lat_coord = element['lat']
                        lon_coord = element['lon']
                    elif 'center' in element:
                        lat_coord = element['center']['lat']
                        lon_coord = element['center']['lon']
                    else:
                        continue
                    
                    # Build address
                    address_parts = []
                    for addr_key in ['addr:housenumber', 'addr:street', 'addr:city']:
                        if addr_key in tags:
                            address_parts.append(tags[addr_key])
                    
                    businesses.append({
                        'name': name,
                        'type': business_type,
                        'latitude': lat_coord,
                        'longitude': lon_coord,
                        'address': ', '.join(address_parts) if address_parts else '',
                        'phone': tags.get('phone', ''),
                        'website': tags.get('website', ''),
                        'description': tags.get('description', '')
                    })
                
                return businesses
            
            return []
            
        except Exception as e:
            self.stdout.write(f'API Error: {str(e)}')
            return []
    
    def get_category_for_business(self, business_type):
        """Map business type to category"""
        mapping = {
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
            'fuel': 'Gas Stations',
            'cinema': 'Movie Theaters',
            'theatre': 'Theaters',
            'museum': 'Museums',
            'supermarket': 'Department Stores',
            'clothes': 'Clothing Stores',
            'shoes': 'Shoe Stores',
            'bakery': 'Bakeries',
        }
        
        category_name = mapping.get(business_type, 'Department Stores')
        
        try:
            return Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            return Category.objects.first()  # Fallback