import random
from django.core.management.base import BaseCommand
from django.db import transaction, models
from businesses.models import Country, City, Category, Business
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populate empty categories with realistic businesses across all countries and cities'

    def add_arguments(self, parser):
        parser.add_argument(
            '--categories-per-run',
            type=int,
            default=10,
            help='Number of empty categories to populate per run'
        )
        parser.add_argument(
            '--businesses-per-category-city',
            type=int,
            default=2,
            help='Number of businesses to create per category per city'
        )
        parser.add_argument(
            '--major-cities-only',
            action='store_true',
            help='Only populate businesses in major cities (top 50% by population)'
        )

    def handle(self, *args, **options):
        categories_per_run = options['categories_per_run']
        businesses_per_category_city = options['businesses_per_category_city']
        major_cities_only = options['major_cities_only']

        # Get empty categories
        empty_categories = Category.objects.filter(businesses__isnull=True).distinct()
        
        if not empty_categories.exists():
            self.stdout.write(self.style.WARNING('No empty categories found!'))
            return

        self.stdout.write(f'Found {empty_categories.count()} empty categories')
        
        # Limit to specified number of categories
        categories_to_populate = empty_categories[:categories_per_run]
        
        # Get cities to populate
        if major_cities_only:
            # Get top cities by business count as a proxy for size
            cities = list(City.objects.annotate(
                business_count=models.Count('businesses')
            ).order_by('-business_count')[:int(City.objects.count() * 0.5)])
        else:
            cities = list(City.objects.all())

        self.stdout.write(f'Will populate {len(cities)} cities')

        total_created = 0

        with transaction.atomic():
            for category in categories_to_populate:
                category_created = 0
                
                self.stdout.write(f'\\nPopulating category: {category.name}')
                
                for city in cities:
                    # Create businesses for this category in this city
                    for i in range(businesses_per_category_city):
                        business = self.create_business(category, city, i + 1)
                        if business:
                            category_created += 1
                            total_created += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f'  Created {category_created} businesses for {category.name}'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\\n✅ Successfully created {total_created} businesses across {categories_per_run} categories!'
            )
        )

    def create_business(self, category, city, number):
        """Create a realistic business for the given category and city"""
        
        # Business name templates by category
        business_templates = {
            # Restaurants & Food
            'restaurants': ['{city} {type} Restaurant', '{adjective} {type} Kitchen', 'The {adjective} {type}'],
            'pizza-restaurants': ['{city} Pizza', '{adjective} Pizza House', '{name}\\s Pizzeria'],
            'italian-restaurants': ['Trattoria {name}', 'Ristorante {city}', '{adjective} Italian Kitchen'],
            'french-restaurants': ['Bistro {name}', 'Le {adjective}', 'Brasserie {city}'],
            'asian-restaurants': ['{city} Asian Kitchen', '{adjective} Wok', 'Golden {type}'],
            'mexican-restaurants': ['El {name}', '{city} Cantina', '{adjective} Mexican Grill'],
            'seafood-restaurants': ['{city} Seafood House', 'The {adjective} Catch', 'Neptune\\s {type}'],
            'vegetarian-restaurants': ['Green {type}', '{adjective} Leaf', 'Veggie {city}'],
            'vegan-restaurants': ['Plant {type}', '{adjective} Garden', 'Pure {city}'],
            
            # Hotels & Accommodation
            'luxury-hotels': ['Grand Hotel {city}', 'The {adjective} {city}', '{city} Palace Hotel'],
            'boutique-hotels': ['Boutique {city}', 'The {adjective} House', '{name} Hotel'],
            'budget-hotels': ['{city} Budget Inn', 'Economy {type}', 'Simple Stay {city}'],
            'bed-breakfasts': ['{city} B&B', '{adjective} House B&B', '{name}\\s Bed & Breakfast'],
            'vacation-rentals': ['{city} Holiday Homes', '{adjective} Rentals', '{name} Apartments'],
            'serviced-apartments': ['{city} Serviced Flats', '{adjective} Suites', 'Executive {type}'],
            'camping-sites': ['{city} Camping', '{adjective} Campground', 'Nature {type}'],
            'resort-hotels': ['{city} Resort', '{adjective} Holiday Resort', 'Paradise {type}'],
            
            # Shopping & Retail
            'fashion-boutiques': ['{adjective} Fashion', '{city} Style', 'Boutique {name}'],
            'shoe-stores': ['{city} Shoes', '{adjective} Footwear', '{name} Shoe Store'],
            'bookstores': ['{city} Books', 'The {adjective} Bookshop', '{name}\\s Library'],
            'antique-stores': ['{city} Antiques', '{adjective} Treasures', 'Vintage {type}'],
            
            # Health & Beauty
            'pharmacies': ['{city} Pharmacy', '{adjective} Chemist', '{name} Drugstore'],
            'barber-shops': ['{city} Barber', 'The {adjective} Cut', '{name}\\s Barbershop'],
            'beauty-salons': ['{adjective} Beauty', '{city} Salon', '{name} Beauty Studio'],
            'dental-clinics': ['{city} Dental', 'Dr. {name} Dentist', '{adjective} Dental Care'],
            'medical-clinics': ['{city} Medical Center', 'Dr. {name} Clinic', '{adjective} Health'],
            
            # Entertainment & Nightlife
            'bars-pubs': ['The {adjective} Pub', '{city} Bar', '{name}\\s Tavern'],
            'nightclubs': ['{city} Club', '{adjective} Nights', 'Club {name}'],
            'movie-theaters': ['{city} Cinema', '{adjective} Movies', '{name} Theater'],
            'bowling-alleys': ['{city} Bowling', '{adjective} Lanes', 'Strike {type}'],
            'amusement-parks': ['{city} Fun Park', '{adjective} Adventures', 'Wonder {type}'],
            
            # Automotive
            'auto-repair': ['{city} Auto Repair', '{adjective} Motors', '{name}\\s Garage'],
            'auto-parts-stores': ['{city} Auto Parts', '{adjective} Components', '{name} Parts'],
            'car-dealerships': ['{city} {brand} Dealer', '{adjective} Motors', '{name} Cars'],
            'gas-stations': ['{city} Fuel', '{adjective} Gas', '{name} Station'],
            
            # Professional Services
            'accounting-firms': ['{city} Accounting', '{name} & Associates', '{adjective} Financial'],
            'law-firms': ['{name} Law Office', '{city} Legal', '{adjective} Attorneys'],
            'business-consultants': ['{city} Consulting', '{adjective} Solutions', '{name} Advisory'],
            'architects': ['{name} Architecture', '{city} Design', '{adjective} Architects'],
            'engineering-firms': ['{city} Engineering', '{adjective} Technical', '{name} Engineers'],
            
            # Education
            'language-schools': ['{city} Language Center', '{adjective} Language School', '{name} Institute'],
            'driving-schools': ['{city} Driving', '{adjective} Driver Training', '{name} Driving School'],
            'art-schools': ['{city} Art Academy', '{adjective} Creative Studio', '{name} Arts'],
            
            # Technology
            'software-companies': ['{city} Software', '{adjective} Tech', '{name} Solutions'],
            'web-design': ['{city} Web Design', '{adjective} Digital', '{name} Creative'],
            'it-support': ['{city} IT Support', '{adjective} Tech Services', '{name} Systems'],
        }

        # Adjectives for business names
        adjectives = [
            'Golden', 'Royal', 'Premium', 'Elite', 'Modern', 'Classic', 'Perfect', 'Superior',
            'Excellence', 'Quality', 'Professional', 'Expert', 'Reliable', 'Trusted', 'Premier',
            'Finest', 'Outstanding', 'Exceptional', 'Distinguished', 'Prestigious'
        ]

        # Common names for businesses
        common_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
            'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
            'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson'
        ]

        # Get appropriate template
        category_slug = category.slug
        templates = business_templates.get(category_slug, ['{city} {type}', '{adjective} {type}', '{name}\\s {type}'])
        
        # Choose random template
        template = random.choice(templates)
        
        # Generate name components
        adjective = random.choice(adjectives)
        name = random.choice(common_names)
        type_word = category.name.split()[0] if ' ' in category.name else category.name
        
        # Create business name
        business_name = template.format(
            city=city.name,
            adjective=adjective,
            name=name,
            type=type_word
        )
        
        # Generate realistic contact info
        phone_prefixes = {
            'germany': '+49',
            'spain': '+34', 
            'portugal': '+351',
            'france': '+33',
            'italy': '+39',
            'belgium': '+32',
            'poland': '+48',
            'hungary': '+36',
            'sweden': '+46',
            'austria': '+43',
        }
        
        country_slug = city.country.slug
        prefix = phone_prefixes.get(country_slug, '+44')
        phone = f"{prefix} {random.randint(100, 999)} {random.randint(100000, 999999)}"
        
        # Generate email
        business_slug = slugify(business_name)
        domain_endings = ['.com', '.eu', f".{city.country.code.lower()}"]
        email = f"info@{business_slug}{random.choice(domain_endings)}"
        
        # Create realistic address
        street_numbers = random.randint(1, 999)
        street_names = [
            'Main Street', 'High Street', 'Church Road', 'Market Square', 'Station Road',
            'Park Avenue', 'Oak Street', 'Mill Lane', 'Victoria Road', 'King Street'
        ]
        address = f"{street_numbers} {random.choice(street_names)}"
        
        # Generate description
        descriptions = [
            f"Professional {category.name.lower()} services in {city.name}.",
            f"Quality {category.name.lower()} in the heart of {city.name}.",
            f"Trusted {category.name.lower()} serving {city.name} community.",
            f"Expert {category.name.lower()} with years of experience in {city.name}.",
            f"Premium {category.name.lower()} located in {city.name}, {city.country.name}."
        ]
        description = random.choice(descriptions)
        
        # Check if business with similar name already exists in this city
        existing_slug = slugify(business_name)
        if Business.objects.filter(city=city, slug=existing_slug).exists():
            # Add number to make it unique
            business_name = f"{business_name} {number}"
            existing_slug = slugify(business_name)
        
        try:
            # Create the business
            business = Business.objects.create(
                name=business_name,
                slug=existing_slug,
                category=category,
                city=city,
                address=address,
                phone=phone,
                email=email,
                website=f"https://www.{business_slug}.com",
                description=description,
                is_verified=True,
                is_featured=random.choice([True, False]) if random.random() < 0.1 else False
            )
            
            return business
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating business {business_name}: {str(e)}')
            )
            return None