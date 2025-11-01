#!/usr/bin/env python3
"""
Enhanced Netherlands Business Import Script
Ensures ALL found businesses are imported, not just found
"""
import os
import django
import time
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listacrosseu.settings')
django.setup()

from businesses.models import Business, Country, City, Category
from businesses.google_places_service import GooglePlacesService

# Initialize service
api_key = "AIzaSyBmKk3uM1BZV_qTuodk9fQmYWLzp1J-k48"
google_service = GooglePlacesService(api_key)

def get_or_create_city(city_name, country):
    """Get or create city with proper coordinates"""
    city_coords = {
        'Amsterdam': (52.3676, 4.9041),
        'Rotterdam': (51.9244, 4.4777),
        'Utrecht': (52.0907, 5.1214),
        'Eindhoven': (51.4416, 5.4697),
        'Tilburg': (51.5555, 5.0913),
        'Breda': (51.5719, 4.7683),
        'The Hague': (52.0705, 4.3007),
        'Groningen': (53.2194, 6.5665),
        'Almere': (52.3508, 5.2647),
        'Nijmegen': (51.8426, 5.8518),
        'Enschede': (52.2215, 6.8937),
        'Haarlem': (52.3874, 4.6462),
        'Arnhem': (51.9851, 5.8987),
        'Amersfoort': (52.1561, 5.3878),
        'Zaanstad': (52.4391, 4.8275),
        'Apeldoorn': (52.2112, 5.9699),
        's-Hertogenbosch': (51.6978, 5.3037),
        'Maastricht': (50.8514, 5.6910)
    }
    
    city, created = City.objects.get_or_create(
        name=city_name,
        country=country,
        defaults={
            'latitude': Decimal(str(city_coords.get(city_name, (52.3676, 4.9041))[0])),
            'longitude': Decimal(str(city_coords.get(city_name, (52.3676, 4.9041))[1]))
        }
    )
    if created:
        print(f"   ✅ Created city: {city_name}")
    return city

def force_create_business(place_data, city, category, attempt=1):
    """Force create business with unique naming if needed"""
    try:
        # Convert coordinates to Decimal
        latitude = Decimal(str(place_data.get('latitude', 0)))
        longitude = Decimal(str(place_data.get('longitude', 0)))
        
        # Create unique name if attempt > 1
        base_name = place_data['name']
        if attempt > 1:
            unique_name = f"{base_name} #{attempt}"
        else:
            unique_name = base_name
            
        # Limit slug length
        slug_base = unique_name.lower().replace(' ', '-').replace('#', '-')[:50]
        
        business = Business.objects.create(
            name=unique_name,
            slug=slug_base,
            address=place_data.get('address', ''),
            phone=place_data.get('phone', ''),
            website=place_data.get('website', ''),
            latitude=latitude,
            longitude=longitude,
            city=city,
            category=category,
            google_place_id=place_data.get('place_id', ''),
            rating=place_data.get('rating', 0),
            user_ratings_total=place_data.get('user_ratings_total', 0),
            price_level=place_data.get('price_level', 0)
        )
        return business
        
    except Exception as e:
        if "UNIQUE constraint failed" in str(e) and attempt < 5:
            return force_create_business(place_data, city, category, attempt + 1)
        else:
            print(f"   ❌ ERROR: {e}")
            return None

def process_search_results(search_term, location, target_count=5):
    """Process search results and ensure all are imported"""
    print(f"\n🔍 Search: {search_term} {location}")
    
    try:
        # Get search results
        places = google_service.search_places(search_term, location)
        
        if not places:
            print("   ❌ No places found")
            return 0
            
        print(f"   Found: {len(places)} businesses")
        
        imported_count = 0
        country = Country.objects.get(code='NL')
        
        for i, place_data in enumerate(places[:target_count], 1):
            print(f"   [{i}] Processing: {place_data['name']}")
            
            try:
                # Get detailed info
                details = google_service.get_place_details(place_data['place_id'])
                if details:
                    place_data.update(details)
                
                # Determine city
                city_name = place_data.get('city', location.split(',')[0].strip())
                city = get_or_create_city(city_name, country)
                
                # Determine category
                category_name = place_data.get('types', [search_term])[0] if place_data.get('types') else search_term
                category, _ = Category.objects.get_or_create(name=category_name.title())
                
                # Force create business
                business = force_create_business(place_data, city, category)
                
                if business:
                    print(f"       ✅ SUCCESS: {business.name} - {city.name}")
                    imported_count += 1
                else:
                    print(f"       ❌ FAILED: {place_data['name']}")
                    
            except Exception as e:
                print(f"       ❌ ERROR processing {place_data.get('name', 'unknown')}: {e}")
                continue
                
            # Small delay to respect API limits
            time.sleep(0.1)
            
        return imported_count
        
    except Exception as e:
        print(f"   ❌ Search error: {e}")
        return 0

def main():
    print("🇳🇱 ENHANCED NETHERLANDS IMPORT")
    print("=" * 60)
    
    # Check current count
    country = Country.objects.get(code='NL')
    current_count = Business.objects.filter(city__country=country).count()
    print(f"📊 Current Netherlands businesses: {current_count}")
    
    # Define searches - expanded list
    searches = [
        # Major cities - restaurants
        ("restaurant", "Amsterdam, Netherlands"),
        ("restaurant", "Rotterdam, Netherlands"),
        ("restaurant", "Utrecht, Netherlands"),
        ("restaurant", "The Hague, Netherlands"),
        ("restaurant", "Eindhoven, Netherlands"),
        ("restaurant", "Tilburg, Netherlands"),
        ("restaurant", "Groningen, Netherlands"),
        
        # Hotels
        ("hotel", "Amsterdam, Netherlands"),
        ("hotel", "Rotterdam, Netherlands"),
        ("hotel", "Utrecht, Netherlands"),
        ("hotel", "Maastricht, Netherlands"),
        
        # Professional services
        ("dentist", "Amsterdam, Netherlands"),
        ("lawyer", "Rotterdam, Netherlands"),
        ("accountant", "Utrecht, Netherlands"),
        ("pharmacy", "Eindhoven, Netherlands"),
        
        # More cities
        ("cafe", "Haarlem, Netherlands"),
        ("restaurant", "Nijmegen, Netherlands"),
        ("hotel", "Arnhem, Netherlands"),
        ("dentist", "Breda, Netherlands"),
        ("gym", "Enschede, Netherlands"),
        
        # Additional coverage
        ("restaurant", "Almere, Netherlands"),
        ("cafe", "Amersfoort, Netherlands"),
        ("hotel", "Apeldoorn, Netherlands"),
        ("pharmacy", "s-Hertogenbosch, Netherlands"),
    ]
    
    total_imported = 0
    
    for search_term, location in searches:
        imported = process_search_results(search_term, location, 3)  # 3 per search
        total_imported += imported
        
        # Check if we should continue (quota management)
        if total_imported >= 100:  # Limit to prevent quota exhaustion
            print(f"\n⚠️ Reached import limit of 100 businesses")
            break
    
    print("\n" + "=" * 60)
    print(f"🎉 ENHANCED NETHERLANDS IMPORT COMPLETE!")
    print(f"🏢 NEW Netherlands businesses imported: {total_imported}")
    print(f"📈 Total Netherlands businesses: {current_count + total_imported}")
    print("=" * 60)

if __name__ == "__main__":
    main()