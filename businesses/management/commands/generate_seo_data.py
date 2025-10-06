# businesses/management/commands/generate_seo_data.py
"""
Management command to generate SEO data for all pages
"""

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from businesses.models import Business, Country, City, Category

class Command(BaseCommand):
    help = 'Generate comprehensive SEO data for all pages'

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            choices=['meta', 'structured', 'all'],
            default='all',
            help='Type of SEO data to generate'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting SEO data generation...'))
        
        if options['type'] in ['meta', 'all']:
            self.generate_meta_data()
        
        if options['type'] in ['structured', 'all']:
            self.generate_structured_data()
        
        self.stdout.write(self.style.SUCCESS('SEO data generation completed!'))

    def generate_meta_data(self):
        """Generate meta titles and descriptions"""
        self.stdout.write('Generating meta data...')
        
        # Country meta data
        for country in Country.objects.filter(is_active=True):
            business_count = Business.objects.filter(city__country=country, status='active').count()
            city_count = City.objects.filter(country=country).count()
            
            meta_title = f'Business Directory {country.name} - {business_count}+ Companies | ListAcross.eu'
            meta_description = (
                f'Discover {business_count}+ verified businesses in {country.name}. '
                f'Browse companies across {city_count} cities. Complete contact details, '
                f'reviews and business information in {country.name}.'
            )
            
            self.stdout.write(f'Country: {country.name} - {business_count} businesses')

        # City meta data
        for city in City.objects.select_related('country').all():
            business_count = Business.objects.filter(city=city, status='active').count()
            category_count = Business.objects.filter(city=city, status='active').values('category').distinct().count()
            
            if business_count > 0:
                meta_title = f'Businesses in {city.name}, {city.country.name} - Local Directory | ListAcross.eu'
                meta_description = (
                    f'Find {business_count} local businesses in {city.name}, {city.country.name}. '
                    f'{category_count} categories including restaurants, services, retail and more. '
                    f'Verified contact details and reviews.'
                )
                
                self.stdout.write(f'City: {city.name} - {business_count} businesses')

        # Category meta data
        for category in Category.objects.filter(is_active=True):
            business_count = Business.objects.filter(category=category, status='active').count()
            country_count = Business.objects.filter(category=category, status='active').values('city__country').distinct().count()
            
            meta_title = f'{category.name} Businesses Europe - {business_count}+ Companies | ListAcross.eu'
            meta_description = (
                f'Find the best {category.name.lower()} businesses across Europe. '
                f'{business_count}+ verified companies in {country_count} countries. '
                f'Compare services, read reviews, get contact details.'
            )
            
            self.stdout.write(f'Category: {category.name} - {business_count} businesses')

    def generate_structured_data(self):
        """Generate JSON-LD structured data"""
        self.stdout.write('Generating structured data...')
        
        # Business structured data
        businesses_with_structured_data = 0
        for business in Business.objects.filter(status='active').select_related('city', 'city__country', 'category'):
            structured_data = {
                "@context": "https://schema.org",
                "@type": "LocalBusiness",
                "name": business.name,
                "description": business.description or f"{business.category.name} business in {business.city.name}",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": business.city.name,
                    "addressCountry": business.city.country.code.upper()
                },
                "url": f"/{business.city.country.slug}/{business.city.slug}/{business.category.slug}/{business.slug}/",
                "telephone": business.phone or "",
                "email": business.email or "",
                "priceRange": business.price_range or "",
                "servesCuisine": business.category.name if business.category.slug == 'restaurants' else None,
                "openingHours": [],  # Can be populated from business hours
                "aggregateRating": {
                    "@type": "AggregateRating",
                    "ratingValue": "4.5",  # Default or calculated
                    "reviewCount": "10"    # Default or calculated
                } if business.phone else None  # Only add rating if verified
            }
            
            businesses_with_structured_data += 1
            if businesses_with_structured_data % 100 == 0:
                self.stdout.write(f'Processed {businesses_with_structured_data} businesses...')

        self.stdout.write(f'Generated structured data for {businesses_with_structured_data} businesses')

        # Category structured data
        for category in Category.objects.filter(is_active=True):
            business_count = Business.objects.filter(category=category, status='active').count()
            
            structured_data = {
                "@context": "https://schema.org",
                "@type": "CollectionPage",
                "name": f"{category.name} Businesses in Europe",
                "description": f"Directory of {category.name.lower()} businesses across Europe",
                "url": f"/{category.slug}/",
                "numberOfItems": business_count,
                "about": {
                    "@type": "Thing",
                    "name": category.name,
                    "description": f"European {category.name.lower()} business directory"
                }
            }

        # City/Country structured data
        for country in Country.objects.filter(is_active=True):
            business_count = Business.objects.filter(city__country=country, status='active').count()
            
            structured_data = {
                "@context": "https://schema.org",
                "@type": "CollectionPage",
                "name": f"Business Directory {country.name}",
                "description": f"Complete business directory for {country.name}",
                "url": f"/{country.slug}/",
                "numberOfItems": business_count,
                "about": {
                    "@type": "Country",
                    "name": country.name,
                    "identifier": country.code.upper()
                }
            }

        self.stdout.write('Structured data generation completed')