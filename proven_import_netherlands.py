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

def import_netherlands_businesses():
    """Import Netherlands businesses using proven working method"""
    
    api_key = "AIzaSyBmKk3uM1BZV_qTuodk9fQmYWLzp1J-k48"
    service = GooglePlacesService(api_key)
    User = get_user_model()
    system_user = User.objects.first()
    
    nl = Country.objects.filter(name__icontains='netherlands').first()
    
    print("🇳🇱 NETHERLANDS BUSINESS IMPORT (PROVEN METHOD)")
    print("=" * 60)
    
    current_count = Business.objects.filter(city__country=nl).count()
    print(f"📊 Current Netherlands businesses: {current_count}")
    print(f"🎯 Target: Import ~50 more businesses efficiently")
    
    # Focused search list for diverse Netherlands coverage
    searches = [
        # Amsterdam area
        "restaurant Amsterdam, Netherlands",
        "hotel Amsterdam, Netherlands", 
        "cafe Amsterdam, Netherlands",
        "dentist Amsterdam, Netherlands",
        
        # Rotterdam area  
        "restaurant Rotterdam, Netherlands",
        "hotel Rotterdam, Netherlands",
        "gym Rotterdam, Netherlands",
        
        # Utrecht area
        "restaurant Utrecht, Netherlands",
        "cafe Utrecht, Netherlands",
        "lawyer Utrecht, Netherlands",
        
        # The Hague
        "restaurant The Hague, Netherlands",
        "hotel The Hague, Netherlands",
        
        # Eindhoven (North Brabant - user priority)
        "restaurant Eindhoven, Netherlands",
        "cafe Eindhoven, Netherlands",
        "pharmacy Eindhoven, Netherlands",
        
        # Tilburg (North Brabant)
        "restaurant Tilburg, Netherlands",
        "hotel Tilburg, Netherlands",
        
        # Breda (North Brabant)
        "restaurant Breda, Netherlands",
        "dentist Breda, Netherlands",
        
        # Other major cities
        "restaurant Groningen, Netherlands",
        "hotel Nijmegen, Netherlands",
        "cafe Arnhem, Netherlands",
        "restaurant Enschede, Netherlands"
    ]
    
    imported_count = 0
    target_total = 50
    
    for search_query in searches:
        print(f"\n🔍 Search: {search_query}")
        
        try:
            results = service.search_places(search_query)
            print(f"   Found: {len(results)} businesses")
            
            # Take 2-3 per search to get variety
            take_count = 2 if imported_count > 30 else 3
            
            for i, place in enumerate(results[:take_count]):
                try:
                    business_name = place.get('displayName', {}).get('text', f'Business_{random.randint(1000,9999)}')
                    
                    print(f"   [{i+1}] Importing: {business_name}")
                    
                    business = create_netherlands_business(place, service, system_user, nl)
                    
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
    print(f"🎉 NETHERLANDS IMPORT COMPLETE!")
    print(f"🏢 Businesses imported: {imported_count}")
    print(f"📈 New Netherlands total: {current_count + imported_count}")
    print(f"🔢 API calls used: ~{len(searches) + imported_count}")
    print(f"💰 Estimated quota remaining: ~{1000 - 374 - (len(searches) + imported_count)}")
    print("=" * 60)
    return imported_count

def create_netherlands_business(place, service, system_user, country):
    """Create Netherlands business using proven working method"""
    try:
        parsed = service.parse_place_data(place)
        name = parsed['name']
        
        # Get city
        city = service.find_or_create_city(parsed['address'])
        if not city:
            # Fallback - create Netherlands cities if needed
            address = parsed.get('address', '')
            city_mapping = {
                'Amsterdam': (Decimal('52.3676'), Decimal('4.9041')),
                'Rotterdam': (Decimal('51.9244'), Decimal('4.4777')),
                'Utrecht': (Decimal('52.0907'), Decimal('5.1214')),
                'Hague': (Decimal('52.0705'), Decimal('4.3007')),
                'Eindhoven': (Decimal('51.4416'), Decimal('5.4697')),
                'Tilburg': (Decimal('51.5555'), Decimal('5.0913')),
                'Breda': (Decimal('51.5719'), Decimal('4.7683')),
                'Groningen': (Decimal('53.2194'), Decimal('6.5665')),
                'Nijmegen': (Decimal('51.8426'), Decimal('5.8518')),
                'Arnhem': (Decimal('51.9851'), Decimal('5.8987')),
                'Enschede': (Decimal('52.2215'), Decimal('6.8937')),
            }
            
            city_name = 'Amsterdam'  # Default
            for city_key, coords in city_mapping.items():
                if city_key in address:
                    city_name = city_key
                    if city_key == 'Hague':
                        city_name = 'The Hague'
                    break
            
            city, created = City.objects.get_or_create(
                name=city_name,
                country=country,
                defaults={'latitude': city_mapping.get(city_key, city_mapping['Amsterdam'])[0], 
                         'longitude': city_mapping.get(city_key, city_mapping['Amsterdam'])[1]}
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
        
        # Generate required fields (like successful Belgium script)
        clean_name = slugify(unique_name).replace('-', '')[:15]
        email = f"info@{clean_name}.com"
        description = f"Professional business in {city.name}, Netherlands"
        
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
    imported = import_netherlands_businesses()
    print(f"\n🚀 SUCCESS: {imported} Netherlands businesses imported using proven method!")