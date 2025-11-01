#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listacrosseu.settings')
django.setup()

from businesses.google_places_service import GooglePlacesService
from businesses.models import Country, City
from django.contrib.auth import get_user_model

def quick_test():
    """Quick test to see what's happening with imports"""
    
    # Test API directly
    api_key = "AIzaSyBmKk3uM1BZV_qTuodk9fQmYWLzp1J-k48"
    service = GooglePlacesService(api_key)
    
    print("🔍 Testing Google Places API directly...")
    
    # Test a simple search
    results = service.search_places("restaurant", "Amsterdam, Netherlands")
    print(f"📊 Found {len(results)} places from API")
    
    if results:
        print("✅ First result:")
        first = results[0]
        print(f"   Name: {first.get('displayName', {}).get('text', 'No name')}")
        print(f"   Address: {first.get('formattedAddress', 'No address')}")
        print(f"   Type: {first.get('primaryType', 'No type')}")
        
        # Try to create one business
        User = get_user_model()
        system_user = User.objects.first()
        
        print("🔄 Attempting to create business...")
        try:
            # Parse the data first
            parsed = service.parse_place_data(first)
            print(f"   Parsed name: {parsed.get('name')}")
            print(f"   Parsed address: {parsed.get('address')}")
            print(f"   Parsed type: {parsed.get('primary_type')}")
            
            business = service.create_business_from_place(first, system_user)
            if business:
                print(f"✅ SUCCESS! Created: {business.name}")
            else:
                print("❌ Failed to create business (duplicate or error)")
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("❌ No results from API")

if __name__ == "__main__":
    quick_test()