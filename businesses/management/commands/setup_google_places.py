from django.core.management.base import BaseCommand
from businesses.models import Business, Category, City
from django.db.models import Count

class Command(BaseCommand):
    help = 'Check Google Places API setup and show instructions'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Google Places API Setup Check')
        self.stdout.write('=' * 50)
        
        # Check current database state
        total_businesses = Business.objects.count()
        total_categories = Category.objects.count()
        total_cities = City.objects.count()
        
        self.stdout.write(f'📊 Current Database Status:')
        self.stdout.write(f'   Businesses: {total_businesses}')
        self.stdout.write(f'   Categories: {total_categories}')
        self.stdout.write(f'   Cities: {total_cities}')
        self.stdout.write('')
        
        # Check configuration file
        try:
            from businesses.google_places_config import GOOGLE_PLACES_API_KEY
            if GOOGLE_PLACES_API_KEY == "YOUR_API_KEY_HERE":
                self.stdout.write('❌ API Key Not Configured')
            else:
                key_preview = GOOGLE_PLACES_API_KEY[:10] + "..." if len(GOOGLE_PLACES_API_KEY) > 10 else "short key"
                self.stdout.write(f'✅ API Key Found: {key_preview}')
        except ImportError:
            self.stdout.write('❌ Configuration file missing')
        
        self.stdout.write('')
        self.stdout.write('📋 Setup Instructions:')
        self.stdout.write('=' * 30)
        
        self.stdout.write('1. 🌐 Go to Google Cloud Console:')
        self.stdout.write('   https://console.cloud.google.com/')
        self.stdout.write('')
        
        self.stdout.write('2. 📁 Create or Select Project:')
        self.stdout.write('   - Create new project or use existing')
        self.stdout.write('   - Note your project ID')
        self.stdout.write('')
        
        self.stdout.write('3. 🔧 Enable Places API:')
        self.stdout.write('   - Go to "APIs & Services" > "Library"')
        self.stdout.write('   - Search for "Places API (New)"')
        self.stdout.write('   - Click "Enable"')
        self.stdout.write('')
        
        self.stdout.write('4. 🔑 Create API Key:')
        self.stdout.write('   - Go to "APIs & Services" > "Credentials"')
        self.stdout.write('   - Click "Create Credentials" > "API Key"')
        self.stdout.write('   - Copy the generated key')
        self.stdout.write('')
        
        self.stdout.write('5. 🔒 Secure API Key (Recommended):')
        self.stdout.write('   - Click "Restrict Key"')
        self.stdout.write('   - Under "API restrictions": Select "Places API (New)"')
        self.stdout.write('   - Under "Application restrictions": Add your domain')
        self.stdout.write('')
        
        self.stdout.write('6. ⚙️ Configure in Code:')
        self.stdout.write('   - Edit: businesses/google_places_config.py')
        self.stdout.write('   - Replace "YOUR_API_KEY_HERE" with your actual key')
        self.stdout.write('')
        
        self.stdout.write('7. 🚀 Test Import:')
        self.stdout.write('   python manage.py import_google_places --cities 2 --categories 3 --max-businesses 10')
        self.stdout.write('')
        
        self.stdout.write('💡 Tips:')
        self.stdout.write('   - Start small to test (--max-businesses 10)')
        self.stdout.write('   - Places API costs ~$0.017 per search')
        self.stdout.write('   - 1000 searches ≈ $17 (gets ~5000-10000 businesses)')
        self.stdout.write('   - Enable billing in Google Cloud Console')
        self.stdout.write('')
        
        self.stdout.write('🎯 Expected Results:')
        self.stdout.write('   - Real businesses with verified data')
        self.stdout.write('   - Accurate addresses and phone numbers')
        self.stdout.write('   - Proper country codes and contact info')
        self.stdout.write('   - Active, operational businesses only')
        self.stdout.write('')
        
        if total_businesses == 0:
            self.stdout.write('✅ Database is clean and ready for import!')
        else:
            self.stdout.write('⚠️  Database contains existing businesses')
            self.stdout.write('   Consider backing up or cleaning before import')
        
        self.stdout.write('')
        self.stdout.write('Questions? Check Google Places API documentation:')
        self.stdout.write('https://developers.google.com/maps/documentation/places/web-service/overview')