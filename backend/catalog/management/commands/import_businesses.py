from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
import csv
import os
from catalog.models import Category, Business, BusinessCategory
from geo.models import Country, City, Town
from django.utils import timezone


class Command(BaseCommand):
    help = 'Import businesses from CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='data/businesses.csv',
            help='Path to the CSV file relative to project root'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run without making changes to see what would be imported'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        dry_run = options['dry_run']
        
        # Get the absolute path to the CSV file
        csv_path = os.path.join('..', file_path)
        
        if not os.path.exists(csv_path):
            self.stdout.write(
                self.style.ERROR(f'CSV file not found: {csv_path}')
            )
            return

        self.stdout.write(f'Importing businesses from: {csv_path}')
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - No changes will be made'))

        created_countries = set()
        created_cities = set()
        created_categories = set()
        created_businesses = 0
        skipped_businesses = 0

        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row_num, row in enumerate(reader, 1):
                try:
                    # Extract data from CSV row
                    business_id = row['id']
                    name = row['name'].strip()
                    slug = row['slug'].strip()
                    description = row['description'].strip()
                    email = row['email'].strip()
                    phone = row['phone'].strip()
                    website = row['website'].strip()
                    address = row['address'].strip()
                    city_name = row['city_name'].strip()
                    country_name = row['country_name'].strip()
                    postal_code = row['postal_code'].strip()
                    latitude = row['latitude']
                    longitude = row['longitude']
                    category_name = row['category_name'].strip()
                    status = row['status'].strip()
                    created_at = row['created_at']
                    
                    # Skip inactive businesses
                    if status != 'active':
                        skipped_businesses += 1
                        continue
                    
                    if not dry_run:
                        with transaction.atomic():
                            # Get or create country
                            country_code = self.get_country_code(country_name)
                            country, created = Country.objects.get_or_create(
                                code=country_code,
                                defaults={
                                    'names_json': {'en': country_name},
                                    'is_active': True
                                }
                            )
                            if created:
                                created_countries.add(country_name)

                            # Get or create city
                            city_slug = slugify(city_name)
                            city, created = City.objects.get_or_create(
                                country=country,
                                slug=city_slug,
                                defaults={
                                    'name': city_name,
                                    'lat': float(latitude) if latitude else None,
                                    'lng': float(longitude) if longitude else None,
                                    'is_active': True
                                }
                            )
                            if created:
                                created_cities.add(f"{city_name}, {country_name}")

                            # Get or create town (use city center as default)
                            town_slug = f"{city_slug}-center"
                            town, created = Town.objects.get_or_create(
                                city=city,
                                slug=town_slug,
                                defaults={
                                    'name': f"{city_name} Center",
                                    'is_active': True
                                }
                            )

                            # Get or create category
                            category_slug = slugify(category_name)
                            category, created = Category.objects.get_or_create(
                                slug=category_slug,
                                defaults={
                                    'names_json': {'en': category_name},
                                    'is_active': True
                                }
                            )
                            if created:
                                created_categories.add(category_name)

                            # Create business
                            business, created = Business.objects.get_or_create(
                                slug=slug,
                                defaults={
                                    'name': name,
                                    'street': address,
                                    'postcode': postal_code,
                                    'phone': phone,
                                    'email': email,
                                    'website': website,
                                    'town': town,
                                    'country': country,
                                    'city': city,
                                    'lat': float(latitude) if latitude else None,
                                    'lng': float(longitude) if longitude else None,
                                    'status': status,
                                    'created_at': timezone.now(),
                                    'updated_at': timezone.now(),
                                }
                            )

                            if created:
                                # Associate with category
                                BusinessCategory.objects.get_or_create(
                                    business=business,
                                    category=category
                                )
                                created_businesses += 1
                            else:
                                skipped_businesses += 1
                    else:
                        # Dry run - just count
                        created_businesses += 1

                    if row_num % 100 == 0:
                        self.stdout.write(f'Processed {row_num} rows...')

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error processing row {row_num}: {str(e)}')
                    )
                    continue

        # Print summary
        self.stdout.write('\n=== Import Summary ===')
        if not dry_run:
            self.stdout.write(f'Created {len(created_countries)} countries: {", ".join(created_countries)}')
            self.stdout.write(f'Created {len(created_cities)} cities')
            self.stdout.write(f'Created {len(created_categories)} categories: {", ".join(created_categories)}')
        self.stdout.write(f'Created businesses: {created_businesses}')
        self.stdout.write(f'Skipped businesses: {skipped_businesses}')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('This was a dry run - no actual changes were made'))
        else:
            self.stdout.write(self.style.SUCCESS('Import completed successfully!'))

    def get_country_code(self, country_name):
        """Map country names to ISO-2 codes"""
        country_mapping = {
            'Spain': 'ES',
            'France': 'FR', 
            'Germany': 'DE',
            'Netherlands': 'NL',
            'Portugal': 'PT',
            'Belgium': 'BE',
            'Denmark': 'DK',
            'Luxembourg': 'LU',
            'Slovenia': 'SI',
            'Italy': 'IT',
            'United Kingdom': 'GB',
            'United States': 'US',
        }
        return country_mapping.get(country_name, 'XX')  # XX as fallback
        self.stdout.write(f"Countries created: {stats['countries_created']}")
        self.stdout.write(f"Cities created: {stats['cities_created']}")
        self.stdout.write(f"Towns created: {stats['towns_created']}")
        self.stdout.write(f"Categories created: {stats['categories_created']}")
        self.stdout.write(f"Businesses created: {stats['businesses_created']}")
        self.stdout.write(f"Businesses updated: {stats['businesses_updated']}")
        self.stdout.write(f"Business-category links created: {stats['business_categories_created']}")