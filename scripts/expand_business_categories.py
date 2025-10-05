"""
Business Categories Expansion - Comprehensive EU Business Types
Expands categories to cover all major business types across Europe
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listacrosseu.settings')
django.setup()

from businesses.models import Category


class BusinessCategoriesExpander:
    """Expand business categories for comprehensive EU coverage"""
    
    def __init__(self):
        self.added_categories = 0
        self.skipped_categories = 0
    
    def create_comprehensive_categories(self):
        """Create comprehensive business categories for EU directory"""
        
        categories_structure = {
            # TOURISM & HOSPITALITY
            'Tourism & Hospitality': [
                'Hotels & Resorts',
                'Bed & Breakfasts',
                'Hostels',
                'Holiday Rentals',
                'Camping & Glamping',
                'Tour Operators',
                'Travel Agencies',
                'Tourist Information Centers',
                'Tourist Attractions',
                'Museums & Galleries',
                'Theme Parks',
                'City Tours & Guides',
                'Airport Services',
                'Car Rental Services'
            ],
            
            # RESTAURANTS & FOOD
            'Restaurants & Food': [
                'Fine Dining Restaurants',
                'Casual Dining',
                'Fast Food Chains',
                'Pizza & Italian',
                'Asian Cuisine',
                'Mediterranean Food',
                'Local & Traditional Food',
                'Vegetarian & Vegan',
                'Seafood Restaurants',
                'Steakhouses',
                'Cafes & Coffee Shops',
                'Bakeries & Patisseries',
                'Ice Cream Parlors',
                'Food Trucks',
                'Catering Services',
                'Delicatessens',
                'Wine Bars',
                'Breweries & Microbreweries'
            ],
            
            # ENTERTAINMENT & NIGHTLIFE
            'Entertainment & Nightlife': [
                'Nightclubs & Discos',
                'Bars & Pubs',
                'Cocktail Bars',
                'Wine Bars',
                'Beer Gardens',
                'Live Music Venues',
                'Theaters',
                'Cinemas',
                'Casino & Gaming',
                'Comedy Clubs',
                'Karaoke Bars',
                'Strip Clubs',
                'Adult Entertainment'
            ],
            
            # SHOPPING & RETAIL
            'Shopping & Retail': [
                'Shopping Malls',
                'Department Stores',
                'Fashion & Clothing',
                'Shoes & Accessories',
                'Jewelry & Watches',
                'Electronics & Technology',
                'Books & Stationery',
                'Toys & Games',
                'Home & Garden',
                'Furniture Stores',
                'Antiques & Collectibles',
                'Art & Craft Supplies',
                'Sporting Goods',
                'Outdoor Equipment',
                'Supermarkets',
                'Local Markets',
                'Specialty Food Stores',
                'Pharmacies',
                'Optical Services',
                'Gift Shops',
                'Souvenir Shops'
            ],
            
            # HEALTH & WELLNESS
            'Health & Wellness': [
                'Hospitals',
                'Medical Clinics',
                'Dental Clinics',
                'Pharmacies',
                'Optical Services',
                'Physiotherapy',
                'Massage Therapy',
                'Spa & Wellness Centers',
                'Fitness Centers & Gyms',
                'Yoga Studios',
                'Mental Health Services',
                'Alternative Medicine',
                'Veterinary Services',
                'Medical Laboratories'
            ],
            
            # BEAUTY & PERSONAL CARE
            'Beauty & Personal Care': [
                'Hair Salons',
                'Barbershops',
                'Beauty Salons',
                'Nail Salons',
                'Spa Services',
                'Massage Therapy',
                'Tanning Salons',
                'Tattoo & Piercing Studios',
                'Cosmetic Surgery',
                'Dermatology Clinics'
            ],
            
            # SERVICES & PROFESSIONAL
            'Services & Professional': [
                'Banks & Financial Services',
                'Insurance Companies',
                'Real Estate Agencies',
                'Legal Services',
                'Accounting & Tax Services',
                'Consulting Services',
                'Marketing & Advertising',
                'Translation Services',
                'Cleaning Services',
                'Repair Services',
                'Locksmith Services',
                'Security Services',
                'Moving Services',
                'Courier & Delivery',
                'Storage & Warehousing',
                'Employment Agencies',
                'Event Planning',
                'Wedding Services',
                'Photography Services',
                'Printing Services'
            ],
            
            # AUTOMOTIVE
            'Automotive': [
                'Car Dealerships',
                'Used Car Dealers',
                'Car Rental',
                'Auto Repair Shops',
                'Auto Parts Stores',
                'Gas Stations',
                'Car Wash Services',
                'Tire Services',
                'Auto Insurance',
                'Motorcycle Dealers',
                'Boat & Marine Services'
            ],
            
            # EDUCATION & TRAINING
            'Education & Training': [
                'Universities',
                'Schools',
                'Language Schools',
                'Driving Schools',
                'Training Centers',
                'Tutoring Services',
                'Online Education',
                'Vocational Training',
                'Art Schools',
                'Music Schools',
                'Dance Studios',
                'Libraries'
            ],
            
            # SPORTS & RECREATION
            'Sports & Recreation': [
                'Sports Centers',
                'Swimming Pools',
                'Golf Courses',
                'Tennis Courts',
                'Football Clubs',
                'Basketball Courts',
                'Bowling Alleys',
                'Ski Resorts',
                'Water Sports',
                'Adventure Sports',
                'Cycling Tours',
                'Hiking & Trekking',
                'Fishing Charters',
                'Sports Equipment Rental'
            ],
            
            # CONSTRUCTION & HOME SERVICES
            'Construction & Home Services': [
                'General Contractors',
                'Electricians',
                'Plumbers',
                'Painters & Decorators',
                'Carpenters',
                'Roofing Services',
                'HVAC Services',
                'Landscaping & Gardening',
                'Interior Designers',
                'Architects',
                'Home Security',
                'Pest Control',
                'Pool Services',
                'Window Services'
            ],
            
            # TECHNOLOGY & INTERNET
            'Technology & Internet': [
                'Software Companies',
                'Web Development',
                'IT Support Services',
                'Computer Repair',
                'Mobile Phone Repair',
                'Internet Service Providers',
                'Telecommunications',
                'Data Centers',
                'Cybersecurity Services',
                'Digital Marketing',
                'E-commerce Platforms'
            ],
            
            # TRANSPORTATION
            'Transportation': [
                'Taxi Services',
                'Bus Services',
                'Train Services',
                'Airlines',
                'Airport Shuttles',
                'Bike Rental',
                'Scooter Rental',
                'Boat Services',
                'Freight & Logistics',
                'Moving Companies',
                'Parking Services'
            ]
        }
        
        return categories_structure
    
    def add_category(self, name, parent=None, description=""):
        """Add a single category"""
        
        if Category.objects.filter(name=name, parent=parent).exists():
            self.skipped_categories += 1
            return None
        
        try:
            category = Category.objects.create(
                name=name,
                parent=parent,
                description=description,
                is_active=True,
                sort_order=0
            )
            self.added_categories += 1
            return category
            
        except Exception as e:
            print(f"❌ Error adding category '{name}': {e}")
            return None
    
    def run_expansion(self):
        """Run the categories expansion"""
        
        print("🏷️ STARTING BUSINESS CATEGORIES EXPANSION")
        print("=" * 60)
        
        initial_count = Category.objects.count()
        print(f"📊 Starting with {initial_count} categories")
        
        categories_structure = self.create_comprehensive_categories()
        
        for parent_name, subcategories in categories_structure.items():
            print(f"\n📁 Creating parent category: {parent_name}")
            
            # Create or get parent category
            parent_category = self.add_category(
                name=parent_name,
                parent=None,
                description=f"All businesses related to {parent_name.lower()}"
            )
            
            if not parent_category:
                parent_category = Category.objects.get(name=parent_name, parent=None)
            
            # Create subcategories
            for subcategory_name in subcategories:
                subcategory = self.add_category(
                    name=subcategory_name,
                    parent=parent_category,
                    description=f"{subcategory_name} services and businesses"
                )
                
                if subcategory:
                    print(f"  ✅ Added: {subcategory_name}")
                else:
                    print(f"  ⏭️ Skipped: {subcategory_name}")
        
        # Final statistics
        final_count = Category.objects.count()
        parent_count = Category.objects.filter(parent=None).count()
        child_count = Category.objects.filter(parent__isnull=False).count()
        
        print("\n" + "=" * 60)
        print("🎉 BUSINESS CATEGORIES EXPANSION COMPLETED!")
        print(f"📊 Initial categories: {initial_count}")
        print(f"📊 Final categories: {final_count}")
        print(f"✅ Categories added: {self.added_categories}")
        print(f"⏭️ Categories skipped: {self.skipped_categories}")
        print(f"📈 Total increase: {final_count - initial_count}")
        print(f"📁 Parent categories: {parent_count}")
        print(f"📄 Child categories: {child_count}")


if __name__ == "__main__":
    expander = BusinessCategoriesExpander()
    expander.run_expansion()