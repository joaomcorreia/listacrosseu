#!/usr/bin/env python3
"""
Mock Django Server for ListAcross EU Demo
This provides a simple HTTP server that simulates the Django API endpoints
"""

import http.server
import socketserver
import json
from urllib.parse import urlparse, parse_qs
import os
import threading
import webbrowser

PORT = 8000

class MockDjangoHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        
        # Extract language parameter
        lang = query_params.get('lang', ['en'])[0]
        
        if path == '/':
            self.serve_home_page()
        elif path.startswith('/api/v1/businesses'):
            self.serve_businesses_api(lang, query_params)
        elif path.startswith('/api/v1/categories'):
            self.serve_categories_api(lang)
        elif path.startswith('/api/assistant/'):
            self.serve_assistant_api(lang)
        elif path == '/seo/sitemap.xml':
            self.serve_sitemap()
        elif path == '/seo/robots.txt':
            self.serve_robots()
        else:
            self.serve_404()
    
    def serve_home_page(self):
        """Serve the main home page"""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ListAcross EU - Multi-language Business Directory</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }
        .container { max-width: 1200px; margin: 0 auto; }
        .hero { text-align: center; background: white; padding: 40px; border-radius: 8px; margin-bottom: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .hero h1 { color: #2c3e50; margin-bottom: 10px; }
        .hero p { color: #7f8c8d; font-size: 18px; }
        .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 30px 0; }
        .feature { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .feature h3 { color: #3498db; margin-bottom: 10px; }
        .api-demo { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin: 30px 0; }
        .api-demo h3 { color: #3498db; }
        .api-endpoint { background: #34495e; padding: 10px; border-radius: 4px; margin: 10px 0; font-family: 'Courier New', monospace; }
        .language-switcher { background: white; padding: 20px; border-radius: 8px; text-align: center; }
        .lang-btn { display: inline-block; margin: 5px; padding: 10px 15px; background: #3498db; color: white; text-decoration: none; border-radius: 4px; }
        .lang-btn:hover { background: #2980b9; }
        .status { background: #27ae60; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="status">
            🟢 ListAcross EU Backend API Server is Running Successfully!
        </div>
        
        <div class="hero">
            <h1>🌍 ListAcross EU</h1>
            <p>Multi-language Business Directory Platform</p>
            <p><strong>Supporting 7 Languages:</strong> English, French, Dutch, Portuguese, German, Spanish, and Arabic</p>
        </div>
        
        <div class="language-switcher">
            <h3>🔄 Test Language Switching</h3>
            <a href="/api/v1/businesses/?lang=en" class="lang-btn">🇬🇧 English</a>
            <a href="/api/v1/businesses/?lang=fr" class="lang-btn">🇫🇷 Français</a>
            <a href="/api/v1/businesses/?lang=nl" class="lang-btn">🇳🇱 Nederlands</a>
            <a href="/api/v1/businesses/?lang=pt" class="lang-btn">🇵🇹 Português</a>
            <a href="/api/v1/businesses/?lang=de" class="lang-btn">🇩🇪 Deutsch</a>
            <a href="/api/v1/businesses/?lang=es" class="lang-btn">🇪🇸 Español</a>
            <a href="/api/v1/businesses/?lang=ar" class="lang-btn">🇸🇦 العربية</a>
        </div>
        
        <div class="features">
            <div class="feature">
                <h3>✅ Backend Features Implemented</h3>
                <ul>
                    <li>Django REST Framework API</li>
                    <li>Multi-language support (7 languages)</li>
                    <li>User profile with Arabic preferences</li>
                    <li>Language-aware business listings</li>
                    <li>Advanced search functionality</li>
                    <li>Assistant with language support</li>
                    <li>SEO optimization</li>
                </ul>
            </div>
            
            <div class="feature">
                <h3>📊 Database Models</h3>
                <ul>
                    <li>UserProfile with language preferences</li>
                    <li>Business with multi-language descriptions</li>
                    <li>Category with translations</li>
                    <li>Business Images</li>
                    <li>Billing system (subscription plans)</li>
                </ul>
            </div>
            
            <div class="feature">
                <h3>🚀 API Endpoints Ready</h3>
                <ul>
                    <li>/api/v1/businesses/ - Business listings</li>
                    <li>/api/v1/categories/ - Categories</li>
                    <li>/api/assistant/ - Language-aware assistant</li>
                    <li>/accounts/ - User management</li>
                    <li>/seo/ - SEO tools</li>
                </ul>
            </div>
        </div>
        
        <div class="api-demo">
            <h3>🔗 API Endpoints Demo</h3>
            <p>Click these links to test the API endpoints:</p>
            
            <div class="api-endpoint">
                <strong>Business Listings:</strong> 
                <a href="/api/v1/businesses/?lang=fr" style="color: #3498db;">/api/v1/businesses/?lang=fr</a>
            </div>
            
            <div class="api-endpoint">
                <strong>Categories:</strong> 
                <a href="/api/v1/categories/?lang=es" style="color: #3498db;">/api/v1/categories/?lang=es</a>
            </div>
            
            <div class="api-endpoint">
                <strong>Assistant Languages:</strong> 
                <a href="/api/assistant/languages/" style="color: #3498db;">/api/assistant/languages/</a>
            </div>
            
            <div class="api-endpoint">
                <strong>SEO Sitemap:</strong> 
                <a href="/seo/sitemap.xml" style="color: #3498db;">/seo/sitemap.xml</a>
            </div>
        </div>
        
        <div class="feature">
            <h3>💡 Next Steps for Production</h3>
            <ol>
                <li>Set up proper Python environment</li>
                <li>Run: python manage.py migrate</li>
                <li>Create superuser: python manage.py createsuperuser</li>
                <li>Generate translations: python manage.py makemessages</li>
                <li>Start server: python manage.py runserver</li>
                <li>Connect Next.js frontend</li>
            </ol>
        </div>
    </div>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def serve_businesses_api(self, lang, query_params):
        """Serve mock business listings API"""
        
        # Sample business data with translations
        businesses = {
            'en': [
                {
                    "id": 1,
                    "name": "Café de Paris",
                    "localized_description": "Traditional French café in the heart of Paris serving authentic pastries and coffee.",
                    "category_name": "Restaurant",
                    "city": "Paris",
                    "country": "France",
                    "is_featured": True,
                    "is_verified": True,
                    "slug": "cafe-de-paris"
                },
                {
                    "id": 2,
                    "name": "Amsterdam Bike Tours",
                    "localized_description": "Explore Amsterdam's beautiful canals and historic districts on our guided bicycle tours.",
                    "category_name": "Tourism",
                    "city": "Amsterdam",
                    "country": "Netherlands",
                    "is_featured": True,
                    "is_verified": True,
                    "slug": "amsterdam-bike-tours"
                }
            ],
            'fr': [
                {
                    "id": 1,
                    "name": "Café de Paris",
                    "localized_description": "Café français traditionnel au cœur de Paris servant des pâtisseries authentiques et du café.",
                    "category_name": "Restaurant",
                    "city": "Paris",
                    "country": "France",
                    "is_featured": True,
                    "is_verified": True,
                    "slug": "cafe-de-paris"
                },
                {
                    "id": 2,
                    "name": "Amsterdam Bike Tours",
                    "localized_description": "Explorez les beaux canaux d'Amsterdam et les quartiers historiques lors de nos visites guidées à vélo.",
                    "category_name": "Tourisme",
                    "city": "Amsterdam",
                    "country": "Pays-Bas",
                    "is_featured": True,
                    "is_verified": True,
                    "slug": "amsterdam-bike-tours"
                }
            ],
            'ar': [
                {
                    "id": 1,
                    "name": "مقهى باريس",
                    "localized_description": "مقهى فرنسي تقليدي في قلب باريس يقدم المعجنات الأصيلة والقهوة.",
                    "category_name": "مطعم",
                    "city": "باريس",
                    "country": "فرنسا",
                    "is_featured": True,
                    "is_verified": True,
                    "slug": "cafe-de-paris"
                },
                {
                    "id": 2,
                    "name": "جولات أمستردام بالدراجة",
                    "localized_description": "اكتشف قنوات أمستردام الجميلة والأحياء التاريخية في جولاتنا المرشدة بالدراجات.",
                    "category_name": "سياحة",
                    "city": "أمستردام",
                    "country": "هولندا",
                    "is_featured": True,
                    "is_verified": True,
                    "slug": "amsterdam-bike-tours"
                }
            ]
        }
        
        # Get businesses for the requested language, fallback to English
        business_list = businesses.get(lang, businesses['en'])
        
        response_data = {
            "results": business_list,
            "count": len(business_list),
            "language": lang,
            "message": f"Business listings in {lang.upper()}"
        }
        
        self.send_json_response(response_data)
    
    def serve_categories_api(self, lang):
        """Serve mock categories API"""
        
        categories = {
            'en': [
                {"id": 1, "name": "Restaurant", "localized_name": "Restaurant", "slug": "restaurant"},
                {"id": 2, "name": "Tourism", "localized_name": "Tourism", "slug": "tourism"},
                {"id": 3, "name": "Shopping", "localized_name": "Shopping", "slug": "shopping"}
            ],
            'fr': [
                {"id": 1, "name": "Restaurant", "localized_name": "Restaurant", "slug": "restaurant"},
                {"id": 2, "name": "Tourism", "localized_name": "Tourisme", "slug": "tourism"},
                {"id": 3, "name": "Shopping", "localized_name": "Shopping", "slug": "shopping"}
            ],
            'ar': [
                {"id": 1, "name": "Restaurant", "localized_name": "مطعم", "slug": "restaurant"},
                {"id": 2, "name": "Tourism", "localized_name": "سياحة", "slug": "tourism"},
                {"id": 3, "name": "Shopping", "localized_name": "تسوق", "slug": "shopping"}
            ]
        }
        
        category_list = categories.get(lang, categories['en'])
        self.send_json_response(category_list)
    
    def serve_assistant_api(self, lang):
        """Serve mock assistant API"""
        
        if self.path.endswith('/languages/'):
            languages_data = {
                "languages": [
                    {"code": "en", "name": "English", "native_name": "English"},
                    {"code": "fr", "name": "French", "native_name": "Français"},
                    {"code": "nl", "name": "Dutch", "native_name": "Nederlands"},
                    {"code": "pt", "name": "Portuguese", "native_name": "Português"},
                    {"code": "de", "name": "German", "native_name": "Deutsch"},
                    {"code": "es", "name": "Spanish", "native_name": "Español"},
                    {"code": "ar", "name": "Arabic", "native_name": "العربية", "rtl": True}
                ]
            }
            self.send_json_response(languages_data)
        else:
            self.send_json_response({"message": "Assistant API endpoint", "language": lang})
    
    def serve_sitemap(self):
        """Serve XML sitemap"""
        sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>http://localhost:8000/</loc>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>http://localhost:8000/api/v1/businesses/</loc>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
</urlset>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'application/xml')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(sitemap_content.encode())
    
    def serve_robots(self):
        """Serve robots.txt"""
        robots_content = """User-agent: *
Allow: /

Sitemap: http://localhost:8000/seo/sitemap.xml"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(robots_content.encode())
    
    def serve_404(self):
        """Serve 404 page"""
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        error_response = {"error": "Not Found", "message": "The requested endpoint was not found"}
        self.wfile.write(json.dumps(error_response).encode())
    
    def send_json_response(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

def start_server():
    """Start the mock Django server"""
    Handler = MockDjangoHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"🚀 ListAcross EU Mock Server starting...")
            print(f"🌍 Server running at: http://localhost:{PORT}")
            print(f"📋 API Documentation: http://localhost:{PORT}")
            print(f"🔄 Language switching: Add ?lang=fr (or es, ar, etc.) to any API endpoint")
            print(f"🛑 Press Ctrl+C to stop the server")
            print("-" * 60)
            
            # Auto-open browser
            def open_browser():
                import time
                time.sleep(1)
                webbrowser.open(f'http://localhost:{PORT}')
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print(f"\n🛑 Server stopped by user")
    except OSError as e:
        if e.errno == 10048:
            print(f"❌ Port {PORT} is already in use. Please close any other servers on this port.")
        else:
            print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    start_server()