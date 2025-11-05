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

def test_import_5_businesses():
    """Test import of exactly 5 businesses to validate method"""
    
    api_key = "AIzaSyBmKk3uM1BZV_qTuodk9fQmYWLzp1J-k48"
    service = GooglePlacesService(api_key)
    User = get_user_model()
    system_user = User.objects.first()
    
    nl = Country.objects.filter(name__icontains='netherlands').first()
    
    print("🧪 TEST IMPORT - 5 BUSINESSES ONLY")
    print("=" * 50)
    
    current_count = Business.objects.filter(city__country=nl).count()
    print(f"📊 Current Netherlands businesses: {current_count}")
    print(f"🎯 Target: Import exactly 5 businesses for testing")
    
    # MINIMAL search list - just enough to get 5 businesses
    searches = [
        "restaurant Haarlem, Netherlands",  # Should get 3
        "hotel Maastricht, Netherlands"     # Should get 2 more = 5 total
    ]
    
    imported_count = 0
    target_total = 5
    
    for search_query in searches:
        print(f"\n🔍 Search: {search_query}")
        
        try:
            results = service.search_places(search_query)
            print(f"   Found: {len(results)} businesses")
            
            # Calculate how many we need from this search
            remaining_needed = target_total - imported_count
            take_count = min(3, remaining_needed)  # Take max 3 or whatever we need to reach 5
            
            for i, place in enumerate(results[:take_count]):
                try:
                    business_name = place.get('displayName', {}).get('text', f'Business_{random.randint(1000,9999)}')
                    
                    print(f"   [{i+1}] Importing: {business_name}")
                    
                    business = force_create_netherlands_business(place, service, system_user, nl)
                    
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
    
    print("\n" + "=" * 50)
    print(f"🧪 TEST IMPORT COMPLETE!")
    print(f"🏢 Businesses imported: {imported_count}/{target_total}")
    print(f"📈 New Netherlands total: {current_count + imported_count}")
    print(f"🔢 API calls used: ~{len(searches) + imported_count} (search + details)")
    
    if imported_count == target_total:
        print("✅ TEST SUCCESSFUL - Method works, ready for larger imports!")
    else:
        print("⚠️  TEST PARTIAL - Check errors above")
    
    print("=" * 50)
    return imported_count == target_total

def force_create_netherlands_business(place, service, system_user, country):
    """Force create Netherlands business - based on working Belgium pattern"""
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
            elif 'Haarlem' in address:
                city, created = City.objects.get_or_create(
                    name='Haarlem',
                    country=country,
                    defaults={'latitude': Decimal('52.3874'), 'longitude': Decimal('4.6462')}
                )
            elif 'Maastricht' in address:
                city, created = City.objects.get_or_create(
                    name='Maastricht',
                    country=country,
                    defaults={'latitude': Decimal('50.8514'), 'longitude': Decimal('5.6910')}
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
        
        # Get category
        category = service.map_google_type_to_category(parsed['primary_type'])
        if not category:
            category = Category.objects.first()
        
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
            category=category,
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
    success = test_import_5_businesses()
    if success:
        print("\n🚀 Ready to proceed with larger imports using this proven method!")
    else:
        print("\n⛔ Fix issues before proceeding with larger imports!")