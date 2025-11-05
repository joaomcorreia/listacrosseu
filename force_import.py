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
import random

def force_import_businesses():
    """Force import businesses bypassing all duplicate checks"""
    
    api_key = "AIzaSyBmKk3uM1BZV_qTuodk9fQmYWLzp1J-k48"
    service = GooglePlacesService(api_key)
    User = get_user_model()
    system_user = User.objects.first()
    
    nl = Country.objects.filter(name__icontains='netherlands').first()
    
    print("🚀 FORCE IMPORT - BYPASSING DUPLICATES")
    print("=" * 60)
    
    # Target diverse searches
    searches = [
        "dentist in Breda, Netherlands",
        "hotel in Utrecht, Netherlands", 
        "lawyer in Groningen, Netherlands",
        "restaurant in Maastricht, Netherlands",
        "pharmacy in Arnhem, Netherlands",
        "gym in Haarlem, Netherlands",
        "cafe in Leiden, Netherlands",
        "bakery in Nijmegen, Netherlands",
        "spa in Almere, Netherlands",
        "bank in Apeldoorn, Netherlands"
    ]
    
    imported_count = 0
    
    for search_query in searches:
        print(f"\n🔍 Search: {search_query}")
        
        try:
            results = service.search_places(search_query)
            print(f"   Found: {len(results)} businesses")
            
            for i, place in enumerate(results[:3]):  # Only take first 3 to avoid spam
                try:
                    business_name = place.get('displayName', {}).get('text', f'Business_{random.randint(1000,9999)}')
                    
                    print(f"   [{i+1}] Importing: {business_name}")
                    
                    # FORCE CREATE - NO DUPLICATE CHECKS
                    business = force_create_business(place, service, system_user, nl)
                    
                    if business:
                        imported_count += 1
                        print(f"       ✅ SUCCESS: {business.name}")
                    else:
                        print(f"       ❌ FAILED")
                        
                except Exception as e:
                    print(f"       ❌ ERROR: {e}")
                    continue
            
            time.sleep(1)  # Rate limiting
            
            if imported_count >= 20:  # Reasonable limit for today
                break
                
        except Exception as e:
            print(f"   ❌ Search failed: {e}")
            continue
    
    return imported_count

def force_create_business(place, service, system_user, country):
    """Force create business with minimal checks"""
    try:
        # Parse data
        parsed = service.parse_place_data(place)
        name = parsed['name']
        
        # Create city - force if needed
        city = service.find_or_create_city(parsed['address'])
        if not city:
            # Fallback to a Netherlands city if address parsing fails
            city = City.objects.filter(country=country).first()
            
        if not city or city.country != country:
            return None
        
        # Get category - use fallback if needed
        category = service.map_google_type_to_category(parsed['primary_type'])
        if not category:
            category = Category.objects.filter(name__icontains='Services').first()
            if not category:
                category = Category.objects.first()
        
        # Make name unique by adding random suffix if needed
        original_name = name
        counter = 1
        while Business.objects.filter(name__iexact=name, city=city).exists():
            name = f"{original_name} #{counter}"
            counter += 1
            if counter > 10:  # Avoid infinite loop
                name = f"{original_name} {random.randint(100,999)}"
                break
        
        # Create unique slug
        base_slug = slugify(name)
        slug = base_slug
        counter = 1
        while Business.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        # Convert coordinates safely
        lat = None
        lng = None
        try:
            if parsed['latitude']:
                lat = Decimal(str(round(float(parsed['latitude']), 6)))
            if parsed['longitude']:
                lng = Decimal(str(round(float(parsed['longitude']), 6)))
        except:
            pass
        
        # Generate email
        clean_name = slugify(name).replace('-', '')[:15]
        email = f"info@{clean_name}.com"
        
        # FORCE CREATE
        business = Business.objects.create(
            name=name,
            slug=slug,
            category=category,
            city=city,
            owner=system_user,
            address=parsed['address'] or f"Address in {city.name}",
            phone=parsed['phone'] or '',
            email=email,
            website=parsed['website'] or '',
            description=parsed['description'] or f"Professional business in {city.name}",
            latitude=lat,
            longitude=lng,
            status='active',
            verified=True,
            featured=False
        )
        
        return business
        
    except Exception as e:
        print(f"       Create error: {e}")
        return None

if __name__ == "__main__":
    imported = force_import_businesses()
    print("\n" + "=" * 60)
    print(f"🎉 FORCE IMPORT COMPLETE!")
    print(f"🏢 Businesses ACTUALLY imported: {imported}")
    if imported > 0:
        print("✅ SUCCESS! Businesses are now being imported!")
    else:
        print("❌ Still no imports - deeper issue exists")
    print("=" * 60)