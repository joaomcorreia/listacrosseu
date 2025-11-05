#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listacrosseu.settings')
django.setup()

from businesses.google_places_service import GooglePlacesService
from businesses.models import Business
from django.contrib.auth import get_user_model

def test_import_capability():
    """Test if we can actually import businesses"""
    
    print("🔍 TESTING IMPORT CAPABILITY")
    print("=" * 50)
    
    api_key = "AIzaSyBmKk3uM1BZV_qTuodk9fQmYWLzp1J-k48"
    service = GooglePlacesService(api_key)
    User = get_user_model()
    system_user = User.objects.first()
    
    # Test a simple search
    print("📡 Testing API connection...")
    results = service.search_places("restaurant", "Eindhoven, Netherlands")
    print(f"✅ Found {len(results)} businesses from API")
    
    if results:
        first_business = results[0]
        business_name = first_business.get('displayName', {}).get('text', 'Unknown')
        print(f"🏢 First business: {business_name}")
        
        # Check if it already exists
        existing = Business.objects.filter(name__icontains=business_name.split()[0]).first()
        if existing:
            print(f"⚠️  Similar business exists: {existing.name}")
        else:
            print("✅ No similar business found - good for import")
        
        # Try to create one business manually
        print(f"\n🔄 Attempting to import: {business_name}")
        try:
            imported_business = service.create_business_from_place(first_business, system_user)
            if imported_business:
                print(f"🎉 SUCCESS! Imported: {imported_business.name}")
                print(f"📍 Location: {imported_business.city.name}, {imported_business.city.country.name}")
                print(f"🏷️  Category: {imported_business.category.name if imported_business.category else 'None'}")
                return True
            else:
                print("❌ Import returned None - checking why...")
                
                # Debug what's blocking
                parsed = service.parse_place_data(first_business)
                print(f"   Parsed name: {parsed['name']}")
                print(f"   Address: {parsed['address']}")
                
                # Check city creation
                city = service.find_or_create_city(parsed['address'])
                if city:
                    print(f"   ✅ City found/created: {city.name}, {city.country.name}")
                else:
                    print(f"   ❌ City creation failed")
                    return False
                
                # Check category
                category = service.map_google_type_to_category(parsed['primary_type'])
                if category:
                    print(f"   ✅ Category mapped: {category.name}")
                else:
                    print(f"   ❌ No category mapping for: {parsed['primary_type']}")
                    return False
                
                # Check duplicates
                exact_duplicate = Business.objects.filter(name__iexact=parsed['name'], city=city).exists()
                if exact_duplicate:
                    print(f"   ⚠️  Exact duplicate exists in {city.name}")
                else:
                    print(f"   ✅ No exact duplicate found")
                
                return False
                
        except Exception as e:
            print(f"❌ IMPORT ERROR: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    return False

if __name__ == "__main__":
    success = test_import_capability()
    if success:
        print("\n🚀 IMPORT SYSTEM IS WORKING! Ready for bulk import.")
    else:
        print("\n🛠️  IMPORT SYSTEM NEEDS FIXING FIRST!")