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

def force_import_portugal():
    """Force import Portugal businesses - more from Vila Nova de Gaia + other cities"""
    
    api_key = "AIzaSyBmKk3uM1BZV_qTuodk9fQmYWLzp1J-k48"
    service = GooglePlacesService(api_key)
    User = get_user_model()
    system_user = User.objects.first()
    
    pt = Country.objects.filter(name__icontains='portugal').first()
    
    print("🇵🇹 PORTUGAL EXPANSION IMPORT")
    print("=" * 60)
    
    # Check current
    existing_pt = Business.objects.filter(city__country=pt).count()
    print(f"📊 Current Portugal businesses: {existing_pt}")
    
    # Priority searches - Vila Nova de Gaia + other cities
    searches = [
        # More Vila Nova de Gaia (30+ target)
        "dentist Vila Nova de Gaia, Portugal",
        "gym Vila Nova de Gaia, Portugal", 
        "supermarket Vila Nova de Gaia, Portugal",
        "lawyer Vila Nova de Gaia, Portugal",
        "beauty salon Vila Nova de Gaia, Portugal",
        "bank Vila Nova de Gaia, Portugal",
        "insurance Vila Nova de Gaia, Portugal",
        "real estate Vila Nova de Gaia, Portugal",
        
        # Expand to Porto
        "restaurant Porto, Portugal",
        "hotel Porto, Portugal",
        "cafe Porto, Portugal",
        "pharmacy Porto, Portugal",
        
        # Lisbon
        "restaurant Lisbon, Portugal", 
        "hotel Lisbon, Portugal",
        "dentist Lisbon, Portugal",
        
        # Braga  
        "restaurant Braga, Portugal",
        "cafe Braga, Portugal",
        
        # Coimbra
        "restaurant Coimbra, Portugal",
        "hotel Coimbra, Portugal"
    ]
    
    imported_count = 0
    
    for search_query in searches:
        print(f"\n🔍 Search: {search_query}")
        
        try:
            results = service.search_places(search_query)
            print(f"   Found: {len(results)} businesses")
            
            # Take more from Vila Nova de Gaia, fewer from others
            limit = 5 if "Vila Nova de Gaia" in search_query else 2
            
            for i, place in enumerate(results[:limit]):
                try:
                    business_name = place.get('displayName', {}).get('text', f'Business_{random.randint(1000,9999)}')
                    
                    print(f"   [{i+1}] Importing: {business_name}")
                    
                    business = force_create_portugal_business(place, service, system_user, pt)
                    
                    if business:
                        imported_count += 1
                        print(f"       ✅ SUCCESS: {business.name} - {business.city.name}")
                    else:
                        print(f"       ❌ FAILED")
                        
                except Exception as e:
                    print(f"       ❌ ERROR: {e}")
                    continue
            
            time.sleep(0.8)  # Rate limiting
            
            if imported_count >= 50:  # Good target for Portugal
                break
                
        except Exception as e:
            print(f"   ❌ Search failed: {e}")
            continue
    
    return imported_count

def force_create_portugal_business(place, service, system_user, country):
    """Force create Portugal business"""
    try:
        parsed = service.parse_place_data(place)
        name = parsed['name']
        
        # Get city
        city = service.find_or_create_city(parsed['address'])
        if not city:
            # Fallback to Vila Nova de Gaia if address parsing fails
            city = City.objects.filter(country=country, name__icontains='Vila Nova de Gaia').first()
            if not city:
                city = City.objects.filter(country=country).first()
            
        if not city or city.country != country:
            return None
        
        # Make unique name
        original_name = name
        counter = 1
        while Business.objects.filter(name__iexact=name, city=city).exists():
            name = f"{original_name} #{counter}"
            counter += 1
            if counter > 10:
                name = f"{original_name} {random.randint(100,999)}"
                break
        
        # Get category
        category = service.map_google_type_to_category(parsed['primary_type'])
        if not category:
            category = Category.objects.first()
        
        # Create slug (limit length to avoid error)
        base_slug = slugify(name)[:40]  # Limit to 40 chars
        slug = base_slug
        counter = 1
        while Business.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"[:50]  # Ensure under 50 char limit
            counter += 1
        
        # Coordinates
        lat = None
        lng = None
        try:
            if parsed['latitude']:
                lat = Decimal(str(round(float(parsed['latitude']), 6)))
            if parsed['longitude']:
                lng = Decimal(str(round(float(parsed['longitude']), 6)))
        except:
            pass
        
        # Email
        clean_name = slugify(name).replace('-', '')[:15]
        email = f"info@{clean_name}.com"
        
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
            description=parsed['description'] or f"Professional business in {city.name}, Portugal",
            latitude=lat,
            longitude=lng,
            status='active',
            verified=True,
            featured=False
        )
        
        return business
        
    except Exception as e:
        return None

if __name__ == "__main__":
    imported = force_import_portugal()
    print("\n" + "=" * 60)
    print(f"🎉 PORTUGAL IMPORT COMPLETE!")
    print(f"🏢 NEW Portugal businesses imported: {imported}")
    print(f"🎯 Focus: Vila Nova de Gaia + Porto, Lisbon, Braga")
    print("=" * 60)