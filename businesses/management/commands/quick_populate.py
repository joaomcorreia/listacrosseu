import random
from django.core.management.base import BaseCommand
from django.db import transaction, models
from businesses.models import Country, City, Category, Business
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Quick populate priority empty categories with realistic businesses'

    def add_arguments(self, parser):
        parser.add_argument(
            '--priority-categories',
            type=int,
            default=5,
            help='Number of priority empty categories to populate'
        )
        parser.add_argument(
            '--top-cities',
            type=int,
            default=20,
            help='Number of top cities to populate (by existing business count)'
        )

    def handle(self, *args, **options):
        priority_count = options['priority_categories']
        top_cities_count = options['top_cities']

        # Priority categories that should have businesses everywhere
        priority_category_names = [
            'Pharmacies', 'Restaurants', 'Hotels', 'Gas Stations', 'Supermarkets',
            'Banks', 'Cafes', 'Bars & Pubs', 'Pizza Restaurants', 'Italian Restaurants',
            'French Restaurants', 'Medical Clinics', 'Dental Clinics', 'Beauty Salons',
            'Barber Shops', 'Auto Repair', 'Bookstores', 'Fashion Boutiques'
        ]

        # Get empty priority categories
        empty_priority_categories = Category.objects.filter(
            name__in=priority_category_names,
            businesses__isnull=True
        ).distinct()[:priority_count]

        if not empty_priority_categories.exists():
            self.stdout.write(self.style.WARNING('No empty priority categories found!'))
            # Get any empty categories
            empty_priority_categories = Category.objects.filter(
                businesses__isnull=True
            ).distinct()[:priority_count]

        # Get top cities by business count
        top_cities = City.objects.annotate(
            business_count=models.Count('businesses')
        ).order_by('-business_count')[:top_cities_count]

        self.stdout.write(f'Populating {empty_priority_categories.count()} priority categories in {top_cities.count()} top cities')

        total_created = 0

        for category in empty_priority_categories:
                category_created = 0
                
                self.stdout.write(f'\\nPopulating: {category.name}')
                
                for city in top_cities:
                    # Create 1-3 businesses per category per city
                    num_businesses = random.randint(1, 3)
                    
                    for i in range(num_businesses):
                        business = self.create_realistic_business(category, city, i + 1)
                        if business:
                            category_created += 1
                            total_created += 1

                self.stdout.write(
                    self.style.SUCCESS(f'  ✓ Created {category_created} businesses')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\\n🎉 Successfully created {total_created} businesses!')
        )

    def create_realistic_business(self, category, city, number):
        """Create a realistic business name and details"""
        
        # Business name patterns by category
        name_patterns = {
            'pharmacies': ['{city} Pharmacy', '{adjective} Chemist', 'Farmacia {city}', '{name} Drugstore'],
            'restaurants': ['{adjective} Restaurant', '{city} Dining', 'Restaurant {name}', 'The {adjective} Table'],
            'pizza-restaurants': ['{city} Pizza', 'Pizzeria {name}', '{adjective} Pizza House', 'Pizza {city}'],
            'italian-restaurants': ['Trattoria {name}', 'Ristorante {city}', 'Il {adjective}', '{name} Italian'],
            'french-restaurants': ['Bistro {name}', 'Le {adjective}', 'Brasserie {city}', 'Chez {name}'],
            'hotels': ['Hotel {city}', '{adjective} Hotel', 'Grand {city}', '{name} Inn'],
            'gas-stations': ['{city} Fuel', '{brand} Station', '{adjective} Gas', 'Station {city}'],
            'supermarkets': ['{city} Market', '{adjective} Supermarket', '{name} Foods', 'Market {city}'],
            'banks': ['Bank {city}', '{adjective} Bank', '{name} Banking', '{city} Financial'],
            'cafes': ['Café {city}', 'The {adjective} Cup', '{name} Coffee', 'Coffee {city}'],
            'bars-pubs': ['The {adjective} Pub', '{city} Bar', '{name} Tavern', 'Pub {city}'],
            'medical-clinics': ['{city} Medical', 'Dr. {name} Clinic', '{adjective} Health Center', 'Clinic {city}'],
            'dental-clinics': ['{city} Dental', 'Dr. {name} Dentist', '{adjective} Dental Care', 'Dental {city}'],
            'beauty-salons': ['{adjective} Beauty', '{city} Salon', '{name} Beauty Studio', 'Salon {city}'],
            'barber-shops': ['{city} Barber', 'The {adjective} Cut', '{name} Barbershop', 'Barber {city}'],
            'auto-repair': ['{city} Auto Repair', '{name} Motors', '{adjective} Garage', 'Auto {city}'],
            'bookstores': ['{city} Books', 'The {adjective} Bookshop', '{name} Library', 'Books {city}'],
            'fashion-boutiques': ['{adjective} Fashion', '{city} Style', 'Boutique {name}', 'Fashion {city}'],
        }

        # Get patterns for this category
        category_key = category.slug.replace('-', '-')
        patterns = name_patterns.get(category_key, ['{city} {type}', '{adjective} {type}', '{name} {type}'])

        # Name components
        adjectives = ['Golden', 'Royal', 'Central', 'Modern', 'Classic', 'Elite', 'Premium', 'Quality']
        names = ['Silva', 'Santos', 'Costa', 'Pereira', 'Oliveira', 'Ferreira', 'Rodrigues', 'Alves']
        brands = ['Shell', 'BP', 'Total', 'Esso', 'Repsol', 'Galp']

        # Choose pattern and create name
        pattern = random.choice(patterns)
        business_name = pattern.format(
            city=city.name,
            adjective=random.choice(adjectives),
            name=random.choice(names),
            type=category.name,
            brand=random.choice(brands)
        )

        # Create unique slug (must be unique globally, not just per city)
        base_slug = slugify(business_name)
        slug = base_slug
        counter = 1
        while Business.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        # Generate contact info
        country_phones = {
            'germany': '+49', 'spain': '+34', 'portugal': '+351', 'france': '+33',
            'italy': '+39', 'belgium': '+32', 'poland': '+48', 'hungary': '+36',
            'sweden': '+46', 'austria': '+43'
        }
        
        phone_prefix = country_phones.get(city.country.slug, '+44')
        phone = f"{phone_prefix} {random.randint(100, 999)} {random.randint(100000, 999999)}"
        
        email = f"info@{base_slug}.{city.country.code.lower()}"
        website = f"https://www.{base_slug}.com"
        
        # Address
        street_num = random.randint(1, 500)
        streets = ['Main St', 'High St', 'Church Rd', 'Market Sq', 'Central Ave', 'Park St']
        address = f"{street_num} {random.choice(streets)}"

        # Description
        descriptions = [
            f"Professional {category.name.lower()} services in {city.name}.",
            f"Quality {category.name.lower()} serving the {city.name} community.",
            f"Trusted {category.name.lower()} in the heart of {city.name}."
        ]

        try:
            # Need to create with owner
            from accounts.models import CustomUser
            
            # Get or create a default system user for generated businesses
            system_user, created = CustomUser.objects.get_or_create(
                username='system_generator',
                defaults={
                    'email': 'system@listacrosseu.eu',
                    'first_name': 'System',
                    'last_name': 'Generator',
                    'is_staff': True
                }
            )
            
            business = Business.objects.create(
                name=business_name,
                slug=slug,
                category=category,
                city=city,
                owner=system_user,
                address=address,
                phone=phone,
                email=email,
                website=website,
                description=random.choice(descriptions),
                status='active',
                verified=True,
                featured=random.random() < 0.15  # 15% chance of being featured
            )
            
            return business
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating {business_name}: {str(e)}'))
            return None