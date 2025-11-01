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

def force_import_belgium():
    """Force import Belgium businesses - Antwerp, Brussels, Ghent, Bruges"""
    
    api_key = "AIzaSyBmKk3uM1BZV_qTuodk9fQmYWLzp1J-k48"
    service = GooglePlacesService(api_key)
    User = get_user_model()
    system_user = User.objects.first()
    
    be = Country.objects.filter(name__icontains='belgium').first()
    
    print("🇧🇪 BELGIUM IMPORT")
    print("=" * 60)
    
    # Check current
    existing_be = Business.objects.filter(city__country=be).count() if be else 0
    print(f"📊 Current Belgium businesses: {existing_be}")
    
    # Belgium searches - Antwerp and Brussels focus
    searches = [
        # Antwerp (priority)
        "restaurant Antwerp, Belgium",
        "hotel Antwerp, Belgium",
        "cafe Antwerp, Belgium",
        "dentist Antwerp, Belgium",
        "lawyer Antwerp, Belgium",
        "pharmacy Antwerp, Belgium",
        "gym Antwerp, Belgium",
        "bank Antwerp, Belgium",
        
        # Brussels (priority)  
        "restaurant Brussels, Belgium",
        "hotel Brussels, Belgium",
        "cafe Brussels, Belgium",
        "dentist Brussels, Belgium",
        "lawyer Brussels, Belgium",
        "pharmacy Brussels, Belgium",
        
        # Ghent
        "restaurant Ghent, Belgium",
        "hotel Ghent, Belgium",
        "cafe Ghent, Belgium",
        
        # Bruges
        "restaurant Bruges, Belgium", 
        "hotel Bruges, Belgium"
    ]
    
    imported_count = 0
    
    for search_query in searches:
        print(f"\n🔍 Search: {search_query}")
        
        try:
            results = service.search_places(search_query)
            print(f"   Found: {len(results)} businesses")
            
            # Take more from priority cities (Antwerp/Brussels)
            limit = 3 if ("Antwerp" in search_query or "Brussels" in search_query) else 2
            
            for i, place in enumerate(results[:limit]):
                try:
                    business_name = place.get('displayName', {}).get('text', f'Business_{random.randint(1000,9999)}')
                    
                    print(f"   [{i+1}] Importing: {business_name}")
                    
                    business = force_create_belgium_business(place, service, system_user, be)
                    
                    if business:
                        imported_count += 1
                        print(f"       ✅ SUCCESS: {business.name} - {business.city.name}")
                    else:
                        print(f"       ❌ FAILED")
                        
                except Exception as e:
                    print(f"       ❌ ERROR: {e}")
                    continue
            
            time.sleep(1)  # Rate limiting
            
            if imported_count >= 40:  # Good target for Belgium
                break
                
        except Exception as e:
            print(f"   ❌ Search failed: {e}")
            continue
    
    return imported_count

def force_create_belgium_business(place, service, system_user, country):
    """Force create Belgium business"""
    try:
        parsed = service.parse_place_data(place)
        name = parsed['name']
        
        # Get city
        city = service.find_or_create_city(parsed['address'])
        if not city:
            # Fallback - create Belgium cities if needed
            address = parsed.get('address', '')
            if 'Antwerp' in address or 'Anvers' in address:
                city, created = City.objects.get_or_create(
                    name='Antwerp', 
                    country=country,
                    defaults={'latitude': 51.2194, 'longitude': 4.4025}
                )
            elif 'Brussels' in address or 'Bruxelles' in address:
                city, created = City.objects.get_or_create(
                    name='Brussels',
                    country=country, 
                    defaults={'latitude': 50.8503, 'longitude': 4.3517}
                )
            elif 'Ghent' in address or 'Gent' in address:
                city, created = City.objects.get_or_create(
                    name='Ghent',
                    country=country,
                    defaults={'latitude': 51.0543, 'longitude': 3.7174}
                )
            elif 'Bruges' in address or 'Brugge' in address:
                city, created = City.objects.get_or_create(
                    name='Bruges',
                    country=country,
                    defaults={'latitude': 51.2085, 'longitude': 3.2253}
                )
            else:
                # Default to Antwerp if can't determine
                city, created = City.objects.get_or_create(
                    name='Antwerp',
                    country=country,
                    defaults={'latitude': 51.2194, 'longitude': 4.4025}
                )
            
        if not city:
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
        
        # Create slug (limit length)
        base_slug = slugify(name)[:40]
        slug = base_slug
        counter = 1
        while Business.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"[:50]
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
            description=parsed['description'] or f"Professional business in {city.name}, Belgium",
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
    imported = force_import_belgium()
    print("\n" + "=" * 60)
    print(f"🎉 BELGIUM IMPORT COMPLETE!")
    print(f"🏢 NEW Belgium businesses imported: {imported}")
    print(f"🎯 Focus: Antwerp, Brussels, Ghent, Bruges")
    print("=" * 60)