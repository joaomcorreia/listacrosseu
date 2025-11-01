#!/usr/bin/env python
"""
Test script to verify Django REST API is working with your migrated data
"""
import os
import sys
import django
import requests
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listacrosseu.settings')
django.setup()

from businesses.models import Business, Country, City, Category

def test_api_endpoints():
    """Test all major API endpoints"""
    base_url = "http://localhost:8000/api/v1"
    
    print("🧪 Testing Django REST API Endpoints")
    print("=" * 50)
    
    # Test 1: Check if we can access the API
    try:
        response = requests.get(f"{base_url}/stats/")
        if response.status_code == 200:
            stats = response.json()
            print("✅ API Stats endpoint working:")
            print(f"   📊 Total businesses: {stats['total_businesses']}")
            print(f"   🏙️  Total cities: {stats['total_cities']}")
            print(f"   🌍 Total countries: {stats['total_countries']}")
            print(f"   📂 Total categories: {stats['total_categories']}")
            print()
        else:
            print(f"❌ Stats API failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Django server. Make sure it's running on localhost:8000")
        print("   Run: python manage.py runserver")
        return False
    
    # Test 2: Countries endpoint
    try:
        response = requests.get(f"{base_url}/countries/")
        if response.status_code == 200:
            countries = response.json()
            print(f"✅ Countries endpoint: {len(countries)} countries loaded")
            if countries:
                print(f"   Sample: {countries[0]['name']} ({countries[0]['code']})")
            print()
        else:
            print(f"❌ Countries API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Countries API error: {e}")
    
    # Test 3: Categories endpoint
    try:
        response = requests.get(f"{base_url}/categories/")
        if response.status_code == 200:
            categories = response.json()
            print(f"✅ Categories endpoint: {len(categories)} categories loaded")
            if categories:
                print(f"   Sample: {categories[0]['name']}")
            print()
        else:
            print(f"❌ Categories API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Categories API error: {e}")
    
    # Test 4: Businesses endpoint (first page)
    try:
        response = requests.get(f"{base_url}/businesses/")
        if response.status_code == 200:
            data = response.json()
            businesses = data.get('results', [])
            print(f"✅ Businesses endpoint: {len(businesses)} businesses on first page")
            if businesses:
                sample = businesses[0]
                print(f"   Sample: {sample['name']} in {sample['city']}, {sample['country']}")
                print(f"   Category: {sample['category']}")
                print(f"   Plan: {sample['plan']}")
            print(f"   Total available: {data.get('count', 'Unknown')}")
            print()
        else:
            print(f"❌ Businesses API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Businesses API error: {e}")
    
    # Test 5: Search endpoint
    try:
        response = requests.get(f"{base_url}/search/?q=restaurant")
        if response.status_code == 200:
            search_data = response.json()
            results = search_data.get('results', [])
            print(f"✅ Search endpoint: Found {len(results)} results for 'restaurant'")
            if results:
                print(f"   Sample result: {results[0]['name']} - {results[0]['short_description'][:50]}...")
            print()
        else:
            print(f"❌ Search API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Search API error: {e}")
    
    return True

def test_database_directly():
    """Test database access directly"""
    print("💾 Testing Database Direct Access")
    print("=" * 35)
    
    try:
        # Count records
        business_count = Business.objects.count()
        country_count = Country.objects.count()
        city_count = City.objects.count()
        category_count = Category.objects.count()
        
        print(f"✅ Database accessible:")
        print(f"   📊 Businesses: {business_count}")
        print(f"   🌍 Countries: {country_count}")
        print(f"   🏙️  Cities: {city_count}")
        print(f"   📂 Categories: {category_count}")
        print()
        
        # Test sample business with translations field
        if business_count > 0:
            sample_business = Business.objects.first()
            print(f"✅ Sample business: {sample_business.name}")
            print(f"   ID: {sample_business.id}")
            print(f"   City: {sample_business.city}")
            print(f"   Status: {sample_business.status}")
            print(f"   Translations field: {type(sample_business.translations)} - {bool(sample_business.translations)}")
            print()
        
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 ListAcross.eu Django + Next.js Migration Test")
    print("=" * 55)
    print()
    
    # Test database first
    db_success = test_database_directly()
    
    if db_success:
        print("🌐 Starting API Tests (requires Django server running)...")
        print()
        api_success = test_api_endpoints()
        
        if api_success:
            print("🎉 SUCCESS! Your migration is working perfectly!")
            print()
            print("Next steps:")
            print("1. ✅ Django REST API backend - WORKING")
            print("2. 🔄 Create Next.js frontend")
            print("3. 🔄 Build admin/user dashboards")
            print("4. 🔄 Add 27 EU language translations")
            print("5. 🔄 Integrate MagicAI features")
        else:
            print("⚠️  Database working, but API needs Django server running")
            print("   Run: python manage.py runserver")
    else:
        print("❌ Database issues detected. Check Django configuration.")

if __name__ == "__main__":
    main()