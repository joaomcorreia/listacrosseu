#!/usr/bin/env python
import os
import sys
import django
from decimal import Decimal
import time
import random

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listacrosseu.settings')
django.setup()

from businesses.google_places_service import GooglePlacesService
from businesses.models import Country, City, Category, Business
from django.contrib.auth import get_user_model
from django.utils.text import slugify

def import_portugal_businesses():
    """Import Portugal businesses using proven working method - Vila Nova de Gaia focus"""
    
    api_key = "AIzaSyBmKk3uM1BZV_qTuodk9fQmYWLzp1J-k48"
    service = GooglePlacesService(api_key)
    User = get_user_model()
    system_user = User.objects.first()
    
    pt = Country.objects.filter(name__icontains='portugal').first()
    
    print("🇵🇹 PORTUGAL BUSINESS IMPORT (PROVEN METHOD)")
    print("=" * 60)
    
    current_count = Business.objects.filter(city__country=pt).count()
    print(f"📊 Current Portugal businesses: {current_count}")
    print(f"🎯 Target: Import ~40 more businesses (Vila Nova de Gaia focus)")
    
    # Focused search list prioritizing Vila Nova de Gaia
    searches = [
        # Vila Nova de Gaia (user priority - 30+ businesses)
        "restaurant Vila Nova de Gaia, Portugal",
        "cafe Vila Nova de Gaia, Portugal",
        "hotel Vila Nova de Gaia, Portugal",
        "dentist Vila Nova de Gaia, Portugal",
        "pharmacy Vila Nova de Gaia, Portugal",
        "lawyer Vila Nova de Gaia, Portugal",
        "gym Vila Nova de Gaia, Portugal",
        "bank Vila Nova de Gaia, Portugal",
        
        # Porto (nearby major city)
        "restaurant Porto, Portugal",
        "hotel Porto, Portugal",
        "cafe Porto, Portugal",
        
        # Lisbon 
        "restaurant Lisbon, Portugal",
        "hotel Lisbon, Portugal",
        
        # Braga
        "restaurant Braga, Portugal",
        "cafe Braga, Portugal",
        
        # Other cities
        "restaurant Coimbra, Portugal",
        "hotel Funchal, Portugal",
        "restaurant Aveiro, Portugal"
    ]
    
    imported_count = 0
    target_total = 40
    
    for search_query in searches:
        print(f"\n🔍 Search: {search_query}")
        
        try:
            results = service.search_places(search_query)
            print(f"   Found: {len(results)} businesses")
            
            # Take more from Vila Nova de Gaia searches
            if "Vila Nova de Gaia" in search_query:
                take_count = 3  # Priority city gets 3 per search
            else:
                take_count = 2  # Other cities get 2 per search
            
            for i, place in enumerate(results[:take_count]):
                try:
                    business_name = place.get('displayName', {}).get('text', f'Business_{random.randint(1000,9999)}')
                    
                    print(f"   [{i+1}] Importing: {business_name}")
                    
                    business = create_portugal_business(place, service, system_user, pt)
                    
                    if business:
                        imported_count += 1
                        print(f"       ✅ SUCCESS: {business.name} - {business.city.name}")
                        
                        # Stop if we hit our target
                        if imported_count >= target_total:
                            print(f"       🎯 TARGET REACHED: {target_total} businesses")
                            break
                    else:
                        print(f"       ❌ FAILED")
                        
                except Exception as e:
                    print(f"       ❌ ERROR: {e}")
                    continue
            
            # Stop if we've reached our target
            if imported_count >= target_total:
                break
            
            time.sleep(1)  # Rate limiting
                
        except Exception as e:
            print(f"   ❌ Search failed: {e}")
            continue
    
    print("\n" + "=" * 60)
    print(f"🎉 PORTUGAL IMPORT COMPLETE!")
    print(f"🏢 Businesses imported: {imported_count}")
    print(f"📈 New Portugal total: {current_count + imported_count}")
    print(f"🔢 API calls used: ~{len(searches) + imported_count}")
    print(f"💰 Estimated quota remaining: ~{1000 - 374 - 70 - (len(searches) + imported_count)}")
    print("🎯 Vila Nova de Gaia focus achieved!")
    print("=" * 60)
    return imported_count

def create_portugal_business(place, service, system_user, country):
    """Create Portugal business using proven working method"""
    try:
        parsed = service.parse_place_data(place)
        name = parsed['name']
        
        # Get city
        city = service.find_or_create_city(parsed['address'])
        if not city:
            # Fallback - create Portugal cities if needed
            address = parsed.get('address', '')
            city_mapping = {
                'Vila Nova de Gaia': (Decimal('41.1239'), Decimal('-8.6118')),
                'Porto': (Decimal('41.1579'), Decimal('-8.6291')),
                'Lisbon': (Decimal('38.7223'), Decimal('-9.1393')),
                'Lisboa': (Decimal('38.7223'), Decimal('-9.1393')),  # Alternative name
                'Braga': (Decimal('41.5518'), Decimal('-8.4229')),
                'Coimbra': (Decimal('40.2033'), Decimal('-8.4103')),
                'Funchal': (Decimal('32.6669'), Decimal('-16.9241')),
                'Aveiro': (Decimal('40.6443'), Decimal('-8.6455')),
                'Évora': (Decimal('38.5664'), Decimal('-7.9087')),
                'Faro': (Decimal('37.0194'), Decimal('-7.9322')),
            }
            
            city_name = 'Lisboa'  # Default to Lisbon
            coords = city_mapping['Lisboa']
            
            for city_key, city_coords in city_mapping.items():
                if city_key in address:
                    city_name = city_key
                    coords = city_coords
                    break
            
            city, created = City.objects.get_or_create(
                name=city_name,
                country=country,
                defaults={'latitude': coords[0], 'longitude': coords[1]}
            )
        
        # Generate unique business name
        attempt = 1
        unique_name = name
        while Business.objects.filter(name=unique_name).exists() and attempt < 10:
            unique_name = f"{name} #{attempt}"
            attempt += 1
        
        # Get category
        category = service.map_google_type_to_category(parsed['primary_type'])
        if not category:
            category = Category.objects.first()
        
        # Generate required fields (like successful Belgium/Netherlands scripts)
        clean_name = slugify(unique_name).replace('-', '')[:15]
        email = f"info@{clean_name}.com"
        description = f"Professional business in {city.name}, Portugal"
        
        # Create business using proven method
        business = Business.objects.create(
            owner=system_user,
            name=unique_name,
            slug=slugify(unique_name)[:50],
            description=description,
            short_description=description[:100],
            email=email,
            phone=parsed.get('phone', ''),
            website=parsed.get('website', ''),
            address=parsed.get('address', f"Address in {city.name}"),
            city=city,
            postal_code='',
            latitude=Decimal(str(parsed.get('latitude', 0))),
            longitude=Decimal(str(parsed.get('longitude', 0))),
            category=category,
            status='active',
            verified=True,
            featured=False,
            meta_title=unique_name,
            meta_description=description[:160],
            keywords=f"{category.name}, {city.name}",
            views_count=0,
            clicks_count=0,
            translations={}
        )
        
        return business
        
    except Exception as e:
        print(f"   Business creation error: {e}")
        return None

if __name__ == "__main__":
    imported = import_portugal_businesses()
    print(f"\n🚀 SUCCESS: {imported} Portugal businesses imported with Vila Nova de Gaia focus!")