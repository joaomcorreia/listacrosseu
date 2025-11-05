#!/usr/bin/env python3
"""
Enhanced Portugal Business Import Script
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
        'Vila Nova de Gaia': (41.1239, -8.6118),
        'Porto': (41.1579, -8.6291),
        'Lisbon': (38.7223, -9.1393),
        'Braga': (41.5518, -8.4229),
        'Coimbra': (40.2033, -8.4103),
        'Funchal': (32.6669, -16.9241),
        'Aveiro': (40.6443, -8.6455),
        'Évora': (38.5664, -7.9087),
        'Faro': (37.0194, -7.9322),
        'Guimarães': (41.4416, -8.2918),
        'Leiria': (39.7437, -8.8071),
        'Portimão': (37.1364, -8.5376),
        'Setúbal': (38.5244, -8.8882),
        'Viana do Castelo': (41.6938, -8.8342),
        'Vila Real': (41.3006, -7.7447),
        'Viseu': (40.6566, -7.9122)
    }
    
    city, created = City.objects.get_or_create(
        name=city_name,
        country=country,
        defaults={
            'latitude': Decimal(str(city_coords.get(city_name, (38.7223, -9.1393))[0])),
            'longitude': Decimal(str(city_coords.get(city_name, (38.7223, -9.1393))[1]))
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
        country = Country.objects.get(code='PT')
        
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
    print("🇵🇹 ENHANCED PORTUGAL IMPORT")
    print("=" * 60)
    
    # Check current count
    country = Country.objects.get(code='PT')
    current_count = Business.objects.filter(city__country=country).count()
    print(f"📊 Current Portugal businesses: {current_count}")
    
    # Define searches - focus on Vila Nova de Gaia and expansion
    searches = [
        # Vila Nova de Gaia focus (user priority)
        ("restaurant", "Vila Nova de Gaia, Portugal"),
        ("cafe", "Vila Nova de Gaia, Portugal"),
        ("hotel", "Vila Nova de Gaia, Portugal"),
        ("dentist", "Vila Nova de Gaia, Portugal"),
        ("pharmacy", "Vila Nova de Gaia, Portugal"),
        ("lawyer", "Vila Nova de Gaia, Portugal"),
        
        # Porto (nearby major city)
        ("restaurant", "Porto, Portugal"),
        ("hotel", "Porto, Portugal"),
        ("cafe", "Porto, Portugal"),
        ("gym", "Porto, Portugal"),
        
        # Lisbon
        ("restaurant", "Lisbon, Portugal"),
        ("hotel", "Lisbon, Portugal"),
        ("dentist", "Lisbon, Portugal"),
        ("lawyer", "Lisbon, Portugal"),
        
        # Braga
        ("restaurant", "Braga, Portugal"),
        ("cafe", "Braga, Portugal"),
        ("pharmacy", "Braga, Portugal"),
        
        # Other major cities
        ("restaurant", "Coimbra, Portugal"),
        ("hotel", "Funchal, Portugal"),
        ("restaurant", "Aveiro, Portugal"),
        ("cafe", "Faro, Portugal"),
        ("restaurant", "Guimarães, Portugal"),
        ("hotel", "Portimão, Portugal"),
        
        # More coverage
        ("dentist", "Setúbal, Portugal"),
        ("pharmacy", "Leiria, Portugal"),
        ("restaurant", "Viana do Castelo, Portugal"),
    ]
    
    total_imported = 0
    
    for search_term, location in searches:
        imported = process_search_results(search_term, location, 4)  # 4 per search
        total_imported += imported
        
        # Check if we should continue (quota management)
        if total_imported >= 100:  # Limit to prevent quota exhaustion
            print(f"\n⚠️ Reached import limit of 100 businesses")
            break
    
    print("\n" + "=" * 60)
    print(f"🎉 ENHANCED PORTUGAL IMPORT COMPLETE!")
    print(f"🏢 NEW Portugal businesses imported: {total_imported}")
    print(f"📈 Total Portugal businesses: {current_count + total_imported}")
    print("=" * 60)

if __name__ == "__main__":
    main()