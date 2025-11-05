"""
Management command to create sample CSV templates for importing data.
"""

import csv
import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create sample CSV templates for importing data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output-dir',
            type=str,
            default='.',
            help='Directory to create sample CSV files (default: current directory)',
        )

    def handle(self, *args, **options):
        output_dir = options['output_dir']
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Create cities template
        cities_file = os.path.join(output_dir, 'cities_template.csv')
        with open(cities_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'country_code', 'latitude', 'longitude', 'population', 'is_capital'])
            writer.writerow(['Paris', 'FR', '48.8566', '2.3522', '2161000', 'True'])
            writer.writerow(['Berlin', 'DE', '52.5200', '13.4050', '3669491', 'True'])
            writer.writerow(['Rome', 'IT', '41.9028', '12.4964', '2873000', 'True'])
            writer.writerow(['Madrid', 'ES', '40.4168', '-3.7038', '3223000', 'True'])
            writer.writerow(['Vienna', 'AT', '48.2082', '16.3738', '1911000', 'True'])
        
        self.stdout.write(self.style.SUCCESS(f'Created cities template: {cities_file}'))
        
        # Create categories template
        categories_file = os.path.join(output_dir, 'categories_template.csv')
        with open(categories_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'slug', 'description', 'icon', 'parent_slug', 'sort_order'])
            writer.writerow(['Food & Dining', 'food-dining', 'Restaurants and dining establishments', '🍽️', '', '1'])
            writer.writerow(['Restaurants', 'restaurants', 'Full service restaurants', '🍽️', 'food-dining', '1'])
            writer.writerow(['Fast Food', 'fast-food', 'Quick service restaurants', '🍔', 'food-dining', '2'])
            writer.writerow(['Cafes & Coffee', 'cafes-coffee', 'Coffee shops and cafes', '☕', 'food-dining', '3'])
            writer.writerow(['Hotels & Accommodation', 'hotels', 'Lodging and accommodation', '🏨', '', '2'])
            writer.writerow(['Hotels', 'hotels-sub', 'Full service hotels', '🏨', 'hotels', '1'])
            writer.writerow(['Hostels', 'hostels', 'Budget accommodation', '🛏️', 'hotels', '2'])
            writer.writerow(['Shopping', 'shopping', 'Retail stores and shopping', '🛍️', '', '3'])
            writer.writerow(['Services', 'services', 'Professional services', '💼', '', '4'])
        
        self.stdout.write(self.style.SUCCESS(f'Created categories template: {categories_file}'))
        
        # Create businesses template
        businesses_file = os.path.join(output_dir, 'businesses_template.csv')
        with open(businesses_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                'owner_email', 'name', 'slug', 'description', 'short_description', 'email', 'phone', 
                'website', 'address', 'city_name', 'country_code', 'postal_code', 'latitude', 
                'longitude', 'category_slug', 'plan', 'status', 'featured', 'verified',
                'monday_hours', 'tuesday_hours', 'wednesday_hours', 'thursday_hours', 
                'friday_hours', 'saturday_hours', 'sunday_hours', 'meta_title', 
                'meta_description', 'keywords'
            ])
            writer.writerow([
                'admin@listacross.eu', 'Restaurant Le Bernardin', 'le-bernardin', 
                'Exquisite French cuisine in the heart of Paris with Michelin-starred chef and elegant atmosphere.',
                'Michelin-starred French restaurant in Paris',
                'contact@lebernardine.com', '+33123456789', 'https://lebernardine.com',
                '123 Rue de la Paix', 'Paris', 'FR', '75001', '48.8566', '2.3522',
                'restaurants', 'free', 'active', 'true', 'true',
                '12:00-14:00,19:00-22:00', '12:00-14:00,19:00-22:00', '12:00-14:00,19:00-22:00',
                '12:00-14:00,19:00-22:00', '12:00-14:00,19:00-23:00', '19:00-23:00', 'Closed',
                'Le Bernardin - Fine French Dining in Paris', 'Experience exquisite French cuisine at Le Bernardin, Paris premier restaurant',
                'french restaurant, fine dining, paris, michelin star'
            ])
            writer.writerow([
                'admin@listacross.eu', 'Hotel Sacher', 'hotel-sacher',
                'Luxury 5-star hotel in Vienna with traditional Austrian hospitality and world-famous Sacher-Torte.',
                'Luxury 5-star hotel in Vienna',
                'info@sacher.com', '+4315145600', 'https://sacher.com',
                'Philharmoniker Str. 4', 'Vienna', 'AT', '1010', '48.2041', '16.3691',
                'hotels-sub', 'country', 'active', 'true', 'true',
                '24/7', '24/7', '24/7', '24/7', '24/7', '24/7', '24/7',
                'Hotel Sacher Vienna - Luxury 5-Star Hotel', 'Experience luxury at Hotel Sacher Vienna with traditional Austrian hospitality',
                'luxury hotel, vienna, 5-star, austrian hospitality, sacher torte'
            ])
        
        self.stdout.write(self.style.SUCCESS(f'Created businesses template: {businesses_file}'))
        
        # Show instructions
        self.stdout.write(self.style.WARNING('\n=== CSV IMPORT INSTRUCTIONS ==='))
        self.stdout.write('1. Edit the template files with your real data')
        self.stdout.write('2. Import in this order:')
        self.stdout.write('   a) python manage.py import_categories categories_template.csv')
        self.stdout.write('   b) python manage.py import_cities cities_template.csv')
        self.stdout.write('   c) python manage.py import_businesses businesses_template.csv')
        self.stdout.write('')
        self.stdout.write('Use --dry-run flag to test before actual import:')
        self.stdout.write('   python manage.py import_businesses businesses.csv --dry-run')
        self.stdout.write('')
        self.stdout.write('Required data before importing businesses:')
        self.stdout.write('- Countries (already created)')
        self.stdout.write('- Cities (import first)')
        self.stdout.write('- Categories (import first)')
        self.stdout.write('- At least one user (admin@listacross.eu already exists)')
        