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

def force_import_netherlands():
    """Force import Netherlands businesses - expanded cities"""
    
    api_key = "AIzaSyBmKk3uM1BZV_qTuodk9fQmYWLzp1J-k48"
    service = GooglePlacesService(api_key)
    User = get_user_model()
    system_user = User.objects.first()
    
    nl = Country.objects.filter(name__icontains='netherlands').first()
    
    print("🇳🇱 ENHANCED NETHERLANDS IMPORT")
    print("=" * 60)
    
    current_count = Business.objects.filter(city__country=nl).count()
    print(f"📊 Current Netherlands businesses: {current_count}")
    
    searches = [
        # Major cities - restaurants
        "restaurant Amsterdam, Netherlands",
        "restaurant Rotterdam, Netherlands", 
        "restaurant Utrecht, Netherlands",
        "restaurant The Hague, Netherlands",
        "restaurant Eindhoven, Netherlands",
        "restaurant Tilburg, Netherlands",
        "restaurant Groningen, Netherlands",
        "restaurant Almere, Netherlands",
        
        # Hotels 
        "hotel Amsterdam, Netherlands",
        "hotel Rotterdam, Netherlands",
        "hotel Utrecht, Netherlands", 
        "hotel Maastricht, Netherlands",
        "hotel Nijmegen, Netherlands",
        
        # Cafes
        "cafe Amsterdam, Netherlands",
        "cafe Rotterdam, Netherlands",
        "cafe Haarlem, Netherlands",
        "cafe Breda, Netherlands",
        
        # Professional services
        "dentist Amsterdam, Netherlands",
        "dentist Rotterdam, Netherlands",
        "lawyer Utrecht, Netherlands",
        "pharmacy Eindhoven, Netherlands",
        "gym Amsterdam, Netherlands",
        "bank Rotterdam, Netherlands",
        
        # More cities
        "restaurant Arnhem, Netherlands",
        "cafe Enschede, Netherlands",
        "hotel Apeldoorn, Netherlands", 
        "restaurant s-Hertogenbosch, Netherlands"
    ]
    
    imported_count = 0
    
    for search_query in searches:
        print(f"\n🔍 Search: {search_query}")
        
        try:
            results = service.search_places(search_query)
            print(f"   Found: {len(results)} businesses")
            
            for i, place in enumerate(results[:3]):  # 3 per search
                try:
                    business_name = place.get('displayName', {}).get('text', f'Business_{random.randint(1000,9999)}')
                    
                    print(f"   [{i+1}] Importing: {business_name}")
                    
                    business = force_create_netherlands_business(place, service, system_user, nl)
                    
                    if business:
                        imported_count += 1
                        print(f"       ✅ SUCCESS: {business.name} - {business.city.name}")
                    else:
                        print(f"       ❌ FAILED")
                        
                except Exception as e:
                    print(f"       ❌ ERROR: {e}")
                    continue
            
            time.sleep(1)  # Rate limiting
            
            if imported_count >= 75:  # Good target for Netherlands expansion
                break
                
        except Exception as e:
            print(f"   ❌ Search failed: {e}")
            continue
    
    print("\n" + "=" * 60)
    print(f"🎉 ENHANCED NETHERLANDS IMPORT COMPLETE!")
    print(f"🏢 NEW Netherlands businesses imported: {imported_count}")
    print(f"📈 Total Netherlands businesses: {current_count + imported_count}")
    print("=" * 60)

def force_create_netherlands_business(place, service, system_user, country):
    """Force create Netherlands business"""
    try:
        parsed = service.parse_place_data(place)
        name = parsed['name']
        
        # Get city
        city = service.find_or_create_city(parsed['address'])
        if not city:
            # Fallback - create Netherlands cities if needed
            address = parsed.get('address', '')
            if 'Amsterdam' in address:
                city, created = City.objects.get_or_create(
                    name='Amsterdam', 
                    country=country,
                    defaults={'latitude': Decimal('52.3676'), 'longitude': Decimal('4.9041')}
                )
            elif 'Rotterdam' in address:
                city, created = City.objects.get_or_create(
                    name='Rotterdam',
                    country=country, 
                    defaults={'latitude': Decimal('51.9244'), 'longitude': Decimal('4.4777')}
                )
            elif 'Utrecht' in address:
                city, created = City.objects.get_or_create(
                    name='Utrecht',
                    country=country,
                    defaults={'latitude': Decimal('52.0907'), 'longitude': Decimal('5.1214')}
                )
            elif 'Eindhoven' in address:
                city, created = City.objects.get_or_create(
                    name='Eindhoven',
                    country=country,
                    defaults={'latitude': Decimal('51.4416'), 'longitude': Decimal('5.4697')}
                )
            elif 'Hague' in address:
                city, created = City.objects.get_or_create(
                    name='The Hague',
                    country=country,
                    defaults={'latitude': Decimal('52.0705'), 'longitude': Decimal('4.3007')}
                )
            else:
                # Default to Amsterdam if can't determine
                city, created = City.objects.get_or_create(
                    name='Amsterdam',
                    country=country,
                    defaults={'latitude': Decimal('52.3676'), 'longitude': Decimal('4.9041')}
                )
        
        # Generate unique business name
        attempt = 1
        unique_name = name
        while Business.objects.filter(name=unique_name).exists() and attempt < 10:
            unique_name = f"{name} #{attempt}"
            attempt += 1
        
        # Create business
        business = Business.objects.create(
            name=unique_name,
            slug=slugify(unique_name)[:50],
            address=parsed.get('address', ''),
            phone=parsed.get('phone', ''),
            website=parsed.get('website', ''),
            latitude=parsed.get('latitude', 0),
            longitude=parsed.get('longitude', 0),
            city=city,
            category=service.determine_category(parsed),
            google_place_id=parsed.get('place_id', ''),
            rating=parsed.get('rating', 0),
            user_ratings_total=parsed.get('user_ratings_total', 0),
            price_level=parsed.get('price_level', 0),
            created_by=system_user
        )
        
        return business
        
    except Exception as e:
        print(f"   Business creation error: {e}")
        return None

if __name__ == "__main__":
    force_import_netherlands()