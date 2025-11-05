#!/usr/bin/env python
import os
import sys
import django
from decimal import Decimal
import time

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listacrosseu.settings')
django.setup()

from businesses.google_places_service import GooglePlacesService
from businesses.models import Country, City, Category, Business
from django.contrib.auth import get_user_model
from django.utils.text import slugify

def smart_import_netherlands():
    """Smart import targeting less covered cities and categories"""
    
    api_key = "AIzaSyBmKk3uM1BZV_qTuodk9fQmYWLzp1J-k48"
    service = GooglePlacesService(api_key)
    User = get_user_model()
    system_user = User.objects.first()
    
    nl = Country.objects.filter(name__icontains='netherlands').first()
    
    print("🇳🇱 SMART NETHERLANDS IMPORT")
    print("=" * 60)
    
    # Check current coverage
    existing_businesses = Business.objects.filter(city__country=nl)
    print(f"📊 Current Netherlands businesses: {existing_businesses.count()}")
    
    # Cities to focus on (mix of covered and new)
    target_cities = [
        # North Brabant focus
        "Breda, Netherlands",
        "'s-Hertogenbosch, Netherlands", 
        "Helmond, Netherlands",
        "Oss, Netherlands",
        
        # Less covered major cities
        "Utrecht, Netherlands",
        "Groningen, Netherlands", 
        "Maastricht, Netherlands",
        "Arnhem, Netherlands",
        "Haarlem, Netherlands"
    ]
    
    # Categories that might have less coverage
    search_categories = [
        "hotel", "bed and breakfast", "hostel",
        "dentist", "physiotherapist", "veterinarian",
        "lawyer", "notary", "accountant",
        "real estate", "insurance office", 
        "gym", "fitness center", "spa",
        "bookstore", "electronics store", "jewelry store",
        "florist", "pet store", "bicycle shop",
        "car rental", "travel agency", "bank"
    ]
    
    imported_count = 0
    total_found = 0
    
    for city_name in target_cities:
        print(f"\n📍 Processing: {city_name}")
        print("-" * 40)
        
        # Check existing count for this city
        city_obj = City.objects.filter(name__icontains=city_name.split(',')[0], country=nl).first()
        existing_count = Business.objects.filter(city=city_obj).count() if city_obj else 0
        print(f"   Current businesses in city: {existing_count}")
        
        city_imported = 0
        
        for category in search_categories:
            if imported_count >= 100:  # Overall limit
                break
                
            search_term = f"{category} in {city_name}"
            
            try:
                results = service.search_places(search_term)
                total_found += len(results)
                
                if len(results) == 0:
                    continue
                
                print(f"  🔍 {category}: {len(results)} found", end="")
                
                added_this_search = 0
                for place in results[:2]:  # Limit to avoid spam
                    try:
                        if smart_import_business(place, service, system_user, nl):
                            imported_count += 1
                            city_imported += 1
                            added_this_search += 1
                    except Exception as e:
                        continue
                
                print(f" → {added_this_search} imported")
                
                # Rate limiting
                time.sleep(0.3)
                
            except Exception as e:
                print(f"  ❌ {category}: {e}")
                continue
        
        print(f"  ✅ {city_name}: {city_imported} new businesses")
        
        if imported_count >= 100:
            break
    
    return imported_count, total_found

def smart_import_business(place, service, system_user, country):
    """Smart import with better duplicate handling"""
    try:
        parsed = service.parse_place_data(place)
        name = parsed['name']
        
        # Get/create city
        city = service.find_or_create_city(parsed['address'])
        if not city or city.country != country:
            return False
        
        # Smarter duplicate check - only exact name + exact city
        exact_duplicate = Business.objects.filter(
            name__iexact=name, 
            city=city
        ).exists()
        
        if exact_duplicate:
            return False  # Skip exact duplicates
        
        # Very similar name check (to avoid "Restaurant ABC" and "Restaurant A.B.C.")
        very_similar = Business.objects.filter(
            name__icontains=name[:10],  # First 10 chars
            city=city
        ).exists()
        
        if very_similar and len(name) < 20:  # Only for short names
            return False
        
        # Get category
        category = service.map_google_type_to_category(parsed['primary_type'])
        if not category:
            category = Category.objects.filter(name__icontains='Services').first()
            if not category:
                category = Category.objects.first()  # Fallback
        
        # Create unique slug
        base_slug = slugify(name)
        slug = base_slug
        counter = 1
        while Business.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        # Convert coordinates
        lat = Decimal(str(round(float(parsed['latitude']), 6))) if parsed['latitude'] else None
        lng = Decimal(str(round(float(parsed['longitude']), 6))) if parsed['longitude'] else None
        
        # Generate email
        clean_name = slugify(name).replace('-', '')[:20]  # Limit length
        email = f"info@{clean_name}.com"
        
        business = Business.objects.create(
            name=name,
            slug=slug,
            category=category,
            city=city,
            owner=system_user,
            address=parsed['address'],
            phone=parsed['phone'],
            email=email,
            website=parsed['website'],
            description=parsed['description'],
            latitude=lat,
            longitude=lng,
            status='active',
            verified=True,
            featured=False
        )
        
        return True
        
    except Exception as e:
        return False

if __name__ == "__main__":
    imported, found = smart_import_netherlands()
    print("\n" + "=" * 60)
    print(f"🎉 SMART NETHERLANDS IMPORT COMPLETE!")
    print(f"📊 Total found: {found}")
    print(f"🏢 NEW businesses imported: {imported}")
    print(f"📍 Focus: North Brabant + less covered cities")
    print("=" * 60)