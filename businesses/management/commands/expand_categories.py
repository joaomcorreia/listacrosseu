from django.core.management.base import BaseCommand
from businesses.models import Category
import json


class Command(BaseCommand):
    help = 'Expand business categories from current to 200+ comprehensive EU business types'
    
    def __init__(self):
        super().__init__()
        self.added_categories = 0
        self.skipped_categories = 0
        self.errors = 0
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Starting Business Categories Expansion (67 → 200+ categories)')
        )
        
        # Comprehensive EU business categories
        categories_data = [
            # Food & Dining
            {'name': 'Fine Dining Restaurants', 'slug': 'fine-dining-restaurants'},
            {'name': 'Fast Food Restaurants', 'slug': 'fast-food-restaurants'},
            {'name': 'Pizza Restaurants', 'slug': 'pizza-restaurants'},
            {'name': 'Italian Restaurants', 'slug': 'italian-restaurants'},
            {'name': 'French Restaurants', 'slug': 'french-restaurants'},
            {'name': 'Asian Restaurants', 'slug': 'asian-restaurants'},
            {'name': 'Mexican Restaurants', 'slug': 'mexican-restaurants'},
            {'name': 'Seafood Restaurants', 'slug': 'seafood-restaurants'},
            {'name': 'Vegetarian Restaurants', 'slug': 'vegetarian-restaurants'},
            {'name': 'Vegan Restaurants', 'slug': 'vegan-restaurants'},
            {'name': 'Coffee Shops', 'slug': 'coffee-shops'},
            {'name': 'Bakeries', 'slug': 'bakeries'},
            {'name': 'Pastry Shops', 'slug': 'pastry-shops'},
            {'name': 'Ice Cream Shops', 'slug': 'ice-cream-shops'},
            {'name': 'Delicatessens', 'slug': 'delicatessens'},
            {'name': 'Wine Bars', 'slug': 'wine-bars'},
            {'name': 'Beer Gardens', 'slug': 'beer-gardens'},
            {'name': 'Cocktail Bars', 'slug': 'cocktail-bars'},
            {'name': 'Pubs', 'slug': 'pubs'},
            {'name': 'Nightclubs', 'slug': 'nightclubs'},
            
            # Accommodation & Hotels
            {'name': 'Luxury Hotels', 'slug': 'luxury-hotels'},
            {'name': 'Boutique Hotels', 'slug': 'boutique-hotels'},
            {'name': 'Business Hotels', 'slug': 'business-hotels'},
            {'name': 'Budget Hotels', 'slug': 'budget-hotels'},
            {'name': 'Hostels', 'slug': 'hostels'},
            {'name': 'Bed & Breakfasts', 'slug': 'bed-breakfasts'},
            {'name': 'Vacation Rentals', 'slug': 'vacation-rentals'},
            {'name': 'Serviced Apartments', 'slug': 'serviced-apartments'},
            {'name': 'Camping Sites', 'slug': 'camping-sites'},
            {'name': 'Resort Hotels', 'slug': 'resort-hotels'},
            
            # Shopping & Retail
            {'name': 'Department Stores', 'slug': 'department-stores'},
            {'name': 'Fashion Boutiques', 'slug': 'fashion-boutiques'},
            {'name': 'Clothing Stores', 'slug': 'clothing-stores'},
            {'name': 'Shoe Stores', 'slug': 'shoe-stores'},
            {'name': 'Jewelry Stores', 'slug': 'jewelry-stores'},
            {'name': 'Watch Stores', 'slug': 'watch-stores'},
            {'name': 'Luxury Goods', 'slug': 'luxury-goods'},
            {'name': 'Electronics Stores', 'slug': 'electronics-stores'},
            {'name': 'Computer Stores', 'slug': 'computer-stores'},
            {'name': 'Mobile Phone Stores', 'slug': 'mobile-phone-stores'},
            {'name': 'Bookstores', 'slug': 'bookstores'},
            {'name': 'Music Stores', 'slug': 'music-stores'},
            {'name': 'Sporting Goods', 'slug': 'sporting-goods'},
            {'name': 'Outdoor Equipment', 'slug': 'outdoor-equipment'},
            {'name': 'Home & Garden', 'slug': 'home-garden'},
            {'name': 'Furniture Stores', 'slug': 'furniture-stores'},
            {'name': 'Antique Stores', 'slug': 'antique-stores'},
            {'name': 'Art Galleries', 'slug': 'art-galleries'},
            {'name': 'Gift Shops', 'slug': 'gift-shops'},
            {'name': 'Souvenir Shops', 'slug': 'souvenir-shops'},
            
            # Healthcare & Medical
            {'name': 'General Hospitals', 'slug': 'general-hospitals'},
            {'name': 'Private Clinics', 'slug': 'private-clinics'},
            {'name': 'Dental Clinics', 'slug': 'dental-clinics'},
            {'name': 'Eye Care Centers', 'slug': 'eye-care-centers'},
            {'name': 'Pharmacies', 'slug': 'pharmacies'},
            {'name': 'Medical Laboratories', 'slug': 'medical-laboratories'},
            {'name': 'Physiotherapy', 'slug': 'physiotherapy'},
            {'name': 'Mental Health Services', 'slug': 'mental-health-services'},
            {'name': 'Veterinary Clinics', 'slug': 'veterinary-clinics'},
            {'name': 'Alternative Medicine', 'slug': 'alternative-medicine'},
            
            # Professional Services
            {'name': 'Law Firms', 'slug': 'law-firms'},
            {'name': 'Accounting Firms', 'slug': 'accounting-firms'},
            {'name': 'Tax Consultants', 'slug': 'tax-consultants'},
            {'name': 'Financial Advisors', 'slug': 'financial-advisors'},
            {'name': 'Insurance Agencies', 'slug': 'insurance-agencies'},
            {'name': 'Real Estate Agencies', 'slug': 'real-estate-agencies'},
            {'name': 'Marketing Agencies', 'slug': 'marketing-agencies'},
            {'name': 'IT Consultants', 'slug': 'it-consultants'},
            {'name': 'Web Development', 'slug': 'web-development'},
            {'name': 'Graphic Design', 'slug': 'graphic-design'},
            {'name': 'Translation Services', 'slug': 'translation-services'},
            {'name': 'Recruitment Agencies', 'slug': 'recruitment-agencies'},
            {'name': 'Business Consultants', 'slug': 'business-consultants'},
            {'name': 'Architects', 'slug': 'architects'},
            {'name': 'Engineers', 'slug': 'engineers'},
            
            # Beauty & Personal Care
            {'name': 'Hair Salons', 'slug': 'hair-salons'},
            {'name': 'Barber Shops', 'slug': 'barber-shops'},
            {'name': 'Beauty Salons', 'slug': 'beauty-salons'},
            {'name': 'Nail Salons', 'slug': 'nail-salons'},
            {'name': 'Spas', 'slug': 'spas'},
            {'name': 'Massage Centers', 'slug': 'massage-centers'},
            {'name': 'Fitness Centers', 'slug': 'fitness-centers'},
            {'name': 'Yoga Studios', 'slug': 'yoga-studios'},
            {'name': 'Pilates Studios', 'slug': 'pilates-studios'},
            {'name': 'Personal Trainers', 'slug': 'personal-trainers'},
            
            # Automotive
            {'name': 'Car Dealerships', 'slug': 'car-dealerships'},
            {'name': 'Auto Repair Shops', 'slug': 'auto-repair-shops'},
            {'name': 'Car Rental', 'slug': 'car-rental'},
            {'name': 'Gas Stations', 'slug': 'gas-stations'},
            {'name': 'Car Wash', 'slug': 'car-wash'},
            {'name': 'Tire Shops', 'slug': 'tire-shops'},
            {'name': 'Motorcycle Dealers', 'slug': 'motorcycle-dealers'},
            {'name': 'Auto Parts Stores', 'slug': 'auto-parts-stores'},
            {'name': 'Electric Vehicle Charging', 'slug': 'ev-charging'},
            {'name': 'Auto Insurance', 'slug': 'auto-insurance'},
            
            # Education & Training
            {'name': 'Universities', 'slug': 'universities'},
            {'name': 'Business Schools', 'slug': 'business-schools'},
            {'name': 'Language Schools', 'slug': 'language-schools'},
            {'name': 'Driving Schools', 'slug': 'driving-schools'},
            {'name': 'Cooking Schools', 'slug': 'cooking-schools'},
            {'name': 'Dance Studios', 'slug': 'dance-studios'},
            {'name': 'Music Schools', 'slug': 'music-schools'},
            {'name': 'Art Schools', 'slug': 'art-schools'},
            {'name': 'Tutoring Centers', 'slug': 'tutoring-centers'},
            {'name': 'Professional Training', 'slug': 'professional-training'},
            
            # Entertainment & Recreation
            {'name': 'Movie Theaters', 'slug': 'movie-theaters'},
            {'name': 'Concert Halls', 'slug': 'concert-halls'},
            {'name': 'Opera Houses', 'slug': 'opera-houses'},
            {'name': 'Theaters', 'slug': 'theaters'},
            {'name': 'Museums', 'slug': 'museums'},
            {'name': 'Art Galleries', 'slug': 'art-galleries-entertainment'},
            {'name': 'Amusement Parks', 'slug': 'amusement-parks'},
            {'name': 'Casinos', 'slug': 'casinos'},
            {'name': 'Bowling Alleys', 'slug': 'bowling-alleys'},
            {'name': 'Gaming Centers', 'slug': 'gaming-centers'},
            {'name': 'Sports Venues', 'slug': 'sports-venues'},
            {'name': 'Golf Courses', 'slug': 'golf-courses'},
            {'name': 'Tennis Courts', 'slug': 'tennis-courts'},
            {'name': 'Swimming Pools', 'slug': 'swimming-pools'},
            {'name': 'Ski Resorts', 'slug': 'ski-resorts'},
            
            # Transportation
            {'name': 'Airport Services', 'slug': 'airport-services'},
            {'name': 'Train Stations', 'slug': 'train-stations'},
            {'name': 'Bus Terminals', 'slug': 'bus-terminals'},
            {'name': 'Taxi Services', 'slug': 'taxi-services'},
            {'name': 'Ride Sharing', 'slug': 'ride-sharing'},
            {'name': 'Bike Rentals', 'slug': 'bike-rentals'},
            {'name': 'Scooter Rentals', 'slug': 'scooter-rentals'},
            {'name': 'Ferry Services', 'slug': 'ferry-services'},
            {'name': 'Cruise Lines', 'slug': 'cruise-lines'},
            {'name': 'Logistics Companies', 'slug': 'logistics-companies'},
            
            # Home Services
            {'name': 'Cleaning Services', 'slug': 'cleaning-services'},
            {'name': 'Plumbing Services', 'slug': 'plumbing-services'},
            {'name': 'Electrical Services', 'slug': 'electrical-services'},
            {'name': 'HVAC Services', 'slug': 'hvac-services'},
            {'name': 'Landscaping', 'slug': 'landscaping'},
            {'name': 'Pest Control', 'slug': 'pest-control'},
            {'name': 'Moving Services', 'slug': 'moving-services'},
            {'name': 'Home Security', 'slug': 'home-security'},
            {'name': 'Interior Design', 'slug': 'interior-design'},
            {'name': 'Home Renovation', 'slug': 'home-renovation'},
            
            # Financial Services
            {'name': 'Banks', 'slug': 'banks'},
            {'name': 'Credit Unions', 'slug': 'credit-unions'},
            {'name': 'Investment Banks', 'slug': 'investment-banks'},
            {'name': 'Currency Exchange', 'slug': 'currency-exchange'},
            {'name': 'ATMs', 'slug': 'atms'},
            {'name': 'Financial Planning', 'slug': 'financial-planning'},
            {'name': 'Mortgage Brokers', 'slug': 'mortgage-brokers'},
            {'name': 'Cryptocurrency Services', 'slug': 'cryptocurrency-services'},
            {'name': 'Payment Processing', 'slug': 'payment-processing'},
            {'name': 'Microfinance', 'slug': 'microfinance'},
            
            # Technology & Innovation
            {'name': 'Software Development', 'slug': 'software-development'},
            {'name': 'Mobile App Development', 'slug': 'mobile-app-development'},
            {'name': 'Cloud Services', 'slug': 'cloud-services'},
            {'name': 'Cybersecurity', 'slug': 'cybersecurity'},
            {'name': 'Data Analytics', 'slug': 'data-analytics'},
            {'name': 'AI & Machine Learning', 'slug': 'ai-machine-learning'},
            {'name': 'Blockchain Services', 'slug': 'blockchain-services'},
            {'name': 'IoT Solutions', 'slug': 'iot-solutions'},
            {'name': 'Telecommunications', 'slug': 'telecommunications'},
            {'name': 'Internet Providers', 'slug': 'internet-providers'},
            
            # Manufacturing & Industry
            {'name': 'Food Processing', 'slug': 'food-processing'},
            {'name': 'Textile Manufacturing', 'slug': 'textile-manufacturing'},
            {'name': 'Electronics Manufacturing', 'slug': 'electronics-manufacturing'},
            {'name': 'Automotive Manufacturing', 'slug': 'automotive-manufacturing'},
            {'name': 'Chemical Manufacturing', 'slug': 'chemical-manufacturing'},
            {'name': 'Pharmaceutical Manufacturing', 'slug': 'pharmaceutical-manufacturing'},
            {'name': 'Construction Materials', 'slug': 'construction-materials'},
            {'name': 'Renewable Energy', 'slug': 'renewable-energy'},
            {'name': 'Packaging Services', 'slug': 'packaging-services'},
            {'name': 'Quality Control', 'slug': 'quality-control'},
        ]
        
        # Process each category
        for category_data in categories_data:
            try:
                # Check if category already exists
                if Category.objects.filter(name=category_data['name']).exists():
                    self.stdout.write(f'⏭️  Skipped: {category_data["name"]} (already exists)')
                    self.skipped_categories += 1
                    continue
                
                # Create new category
                category = Category.objects.create(
                    name=category_data['name'],
                    slug=category_data['slug']
                )
                
                self.added_categories += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Added: {category_data["name"]}')
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error adding {category_data["name"]}: {str(e)}')
                )
                self.errors += 1
                continue
        
        # Final statistics
        self.stdout.write('\n' + '='*60)
        self.stdout.write(
            self.style.SUCCESS(f'🎉 Business Categories Expansion Complete!')
        )
        self.stdout.write(f'✅ Categories added: {self.added_categories}')
        self.stdout.write(f'⏭️  Categories skipped: {self.skipped_categories}')
        self.stdout.write(f'❌ Errors: {self.errors}')
        
        total_categories = Category.objects.count()
        self.stdout.write(f'📂 Total categories in database: {total_categories}')
        
        if total_categories >= 150:
            self.stdout.write(
                self.style.SUCCESS('🎯 Target achieved: 150+ categories ready for comprehensive business classification!')
            )