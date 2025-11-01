from django.core.management.base import BaseCommand
from django.db import transaction
from catalog.models import Category, Business, BusinessCategory
from geo.models import Country, City, Town
import random


class Command(BaseCommand):
    help = 'Seed database with sample business data based on CSV statistics'

    def handle(self, *args, **options):
        self.stdout.write('Seeding businesses...')
        
        # Business names by category
        business_names = {
            'restaurants': [
                'La Bella Vita', 'Le Petit Bistro', 'The Golden Fork', 'Casa Miguel',
                'Chez Marie', 'Der Goldene Hirsch', 'Il Giardino', 'El Rincón',
                'Le Grand Chef', 'The Corner Café', 'Pizza Roma', 'Tapas Bar',
                'The French Kitchen', 'Bistro Central', 'La Mesa'
            ],
            'hotels': [
                'Hotel Europa', 'Grand Palace', 'City Center Hotel', 'The Plaza',
                'Hotel Majestic', 'Royal Inn', 'Central Hotel', 'Park View Hotel',
                'The Crown', 'Hotel Continental', 'Villa Bella', 'Hotel Imperial',
                'The Riverside', 'Urban Hotel', 'Hotel Splendor'
            ],
            'shops': [
                'Fashion Boutique', 'Style Shop', 'The Corner Store', 'City Mall',
                'Trendy Clothes', 'Fashion Forward', 'Style Central', 'The Shop',
                'Urban Store', 'Fashion Hub', 'Retail World', 'Shopping Center',
                'The Boutique', 'Style Store', 'Fashion Point'
            ],
            'services': [
                'Professional Services', 'City Consulting', 'Expert Solutions', 'Pro Services',
                'Quality Services', 'Professional Care', 'Expert Help', 'Service Pro',
                'Professional Plus', 'Elite Services', 'Service Center', 'Pro Care',
                'Expert Services', 'Quality Pro', 'Professional Hub'
            ]
        }

        # Sample descriptions
        descriptions = [
            "High-quality service provider with years of experience in the industry.",
            "Family-owned business serving the community for over 20 years.",
            "Modern establishment offering premium services and products.",
            "Traditional business with a contemporary approach to customer service.",
            "Award-winning provider known for excellence and innovation.",
        ]

        # Get active countries, cities, categories
        countries = list(Country.objects.filter(is_active=True))
        categories = list(Category.objects.filter(is_active=True))
        
        if not countries or not categories:
            self.stdout.write(
                self.style.ERROR('No countries or categories found. Run seed_countries and seed_categories first.')
            )
            return

        # Business distribution based on CSV stats
        country_distribution = {
            'ES': 2494,  # Spain
            'FR': 2127,  # France  
            'DE': 1710,  # Germany
            'NL': 121,   # Netherlands
            'PT': 94,    # Portugal
            'BE': 40,    # Belgium
        }

        created_count = 0

        with transaction.atomic():
            for country in countries:
                if country.code not in country_distribution:
                    continue
                
                target_count = min(country_distribution[country.code], 50)  # Limit for demo
                cities = list(City.objects.filter(country=country, is_active=True))
                
                if not cities:
                    continue

                for i in range(target_count):
                    # Select random city and create town if needed
                    city = random.choice(cities)
                    towns = list(Town.objects.filter(city=city, is_active=True))
                    
                    if not towns:
                        # Create a default town
                        town = Town.objects.create(
                            name=f"{city.name} Center",
                            slug=f"{city.slug}-center",
                            city=city,
                            is_active=True
                        )
                    else:
                        town = random.choice(towns)

                    # Select random category
                    category = random.choice(categories)
                    category_key = category.slug.replace('-', '_')
                    
                    # Get business name
                    if category_key in business_names:
                        name_options = business_names[category_key]
                    else:
                        name_options = business_names['services']
                    
                    base_name = random.choice(name_options)
                    business_name = f"{base_name} {city.name}"

                    # Create business
                    business = Business.objects.create(
                        name=business_name,
                        slug=f"{base_name.lower().replace(' ', '-')}-{city.slug}",
                        description=random.choice(descriptions),
                        street=f"{random.randint(1, 999)} Main Street",
                        phone=f"+{country.code}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                        email=f"info@{base_name.lower().replace(' ', '')}{city.slug}.com",
                        website=f"https://www.{base_name.lower().replace(' ', '')}{city.slug}.com",
                        town=town,
                        status='active'
                    )

                    # Associate with category
                    BusinessCategory.objects.create(
                        business=business,
                        category=category
                    )

                    created_count += 1

                    if created_count % 100 == 0:
                        self.stdout.write(f'Created {created_count} businesses...')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} businesses')
        )