#!/usr/bin/env python
"""
API Test Script for ListAcross EU
Tests the multi-language API endpoints and functionality
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def test_api_endpoints():
    """Test various API endpoints with different languages"""
    
    print("🌍 ListAcross EU API Test Suite")
    print("=" * 50)
    
    # Test 1: Business listings in different languages
    print("\n1. Testing Business Listings API")
    languages = ['en', 'fr', 'nl', 'pt', 'de', 'es', 'ar']
    
    for lang in languages:
        try:
            response = requests.get(f"{BASE_URL}/api/v1/businesses/?lang={lang}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ {lang.upper()}: {len(data.get('results', []))} businesses found")
            else:
                print(f"   ❌ {lang.upper()}: Error {response.status_code}")
        except Exception as e:
            print(f"   ❌ {lang.upper()}: Connection error - {str(e)}")
    
    # Test 2: Categories API
    print("\n2. Testing Categories API")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/categories/?lang=fr")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Categories API: {len(data)} categories available")
        else:
            print(f"   ❌ Categories API: Error {response.status_code}")
    except Exception as e:
        print(f"   ❌ Categories API: Connection error - {str(e)}")
    
    # Test 3: Search functionality
    print("\n3. Testing Search API")
    search_terms = {
        'en': 'restaurant',
        'fr': 'restaurant',
        'es': 'restaurante',
        'de': 'restaurant',
        'ar': 'مطعم'
    }
    
    for lang, term in search_terms.items():
        try:
            response = requests.get(f"{BASE_URL}/api/v1/businesses/search/?q={term}&lang={lang}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ {lang.upper()} search '{term}': {data.get('count', 0)} results")
            else:
                print(f"   ❌ {lang.upper()} search: Error {response.status_code}")
        except Exception as e:
            print(f"   ❌ {lang.upper()} search: Connection error - {str(e)}")
    
    # Test 4: Assistant API (requires authentication)
    print("\n4. Testing Assistant Languages API")
    try:
        response = requests.get(f"{BASE_URL}/api/assistant/languages/")
        if response.status_code == 200:
            data = response.json()
            languages = data.get('languages', [])
            print(f"   ✅ Assistant supports {len(languages)} languages:")
            for lang in languages:
                rtl_indicator = " (RTL)" if lang.get('rtl') else ""
                print(f"      - {lang['native_name']} ({lang['code']}){rtl_indicator}")
        else:
            print(f"   ❌ Assistant Languages: Error {response.status_code}")
    except Exception as e:
        print(f"   ❌ Assistant Languages: Connection error - {str(e)}")
    
    # Test 5: SEO endpoints
    print("\n5. Testing SEO Endpoints")
    seo_endpoints = [
        ("/seo/robots.txt", "Robots.txt"),
        ("/seo/sitemap.xml", "Sitemap")
    ]
    
    for endpoint, name in seo_endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            if response.status_code == 200:
                print(f"   ✅ {name}: Available")
            else:
                print(f"   ❌ {name}: Error {response.status_code}")
        except Exception as e:
            print(f"   ❌ {name}: Connection error - {str(e)}")
    
    print("\n" + "=" * 50)
    print("🏁 API Test Complete")
    print(f"⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def test_language_switching():
    """Test language switching functionality"""
    print("\n🔄 Language Switching Test")
    print("-" * 30)
    
    # Test with different Accept-Language headers
    headers_tests = [
        {'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8'},
        {'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8'},
        {'Accept-Language': 'de-DE,de;q=0.9,en;q=0.8'},
        {'Accept-Language': 'ar-SA,ar;q=0.9,en;q=0.8'},
    ]
    
    for headers in headers_tests:
        try:
            response = requests.get(f"{BASE_URL}/api/v1/businesses/", headers=headers)
            lang_header = headers['Accept-Language'].split(',')[0].split('-')[0]
            if response.status_code == 200:
                print(f"   ✅ Accept-Language {lang_header}: Server responded correctly")
            else:
                print(f"   ❌ Accept-Language {lang_header}: Error {response.status_code}")
        except Exception as e:
            print(f"   ❌ Accept-Language test: Connection error - {str(e)}")

def print_sample_usage():
    """Print sample API usage examples"""
    print("\n📚 Sample API Usage")
    print("-" * 30)
    
    examples = [
        "# Get businesses in French",
        "GET /api/v1/businesses/?lang=fr",
        "",
        "# Search for restaurants in Spanish",
        "GET /api/v1/businesses/search/?q=restaurante&lang=es",
        "",
        "# Get categories in Arabic",
        "GET /api/v1/categories/?lang=ar",
        "",
        "# Update user language preferences (requires auth)",
        "POST /accounts/set-language/",
        "Content-Type: application/json",
        "{",
        '  "preferred_language": "fr",',
        '  "arabic_on_dashboard": false,',
        '  "arabic_on_website": true"',
        "}",
        "",
        "# Chat with assistant in user's language (requires auth)",
        "POST /api/assistant/chat/",
        "Content-Type: application/json",
        "{",
        '  "message": "Hello, can you help me find restaurants?",',
        '  "context": "website"',
        "}",
    ]
    
    for line in examples:
        print(f"   {line}")

if __name__ == "__main__":
    print("Starting ListAcross EU API Tests...")
    print("Make sure the Django development server is running on http://127.0.0.1:8000")
    print()
    
    try:
        test_api_endpoints()
        test_language_switching()
        print_sample_usage()
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
    
    print("\n💡 To run the Django server:")
    print("   python manage.py runserver")
    print("\n💡 To create test data:")
    print("   python manage.py shell")
    print("   # Then create some Category and Business objects")