from django.core.management.base import BaseCommand
from django.core import serializers
from businesses.models import Business, City, Country, Category
import json
import csv
import os
from datetime import datetime


class Command(BaseCommand):
    help = 'Export all business data for migration to new framework'

    def add_arguments(self, parser):
        parser.add_argument(
            '--format',
            type=str,
            choices=['json', 'csv', 'both'],
            default='both',
            help='Export format (json, csv, or both)'
        )
        parser.add_argument(
            '--output-dir',
            type=str,
            default='data_export',
            help='Output directory for exported files'
        )

    def handle(self, *args, **options):
        output_dir = options['output_dir']
        export_format = options['format']
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        self.stdout.write(
            self.style.SUCCESS(f'Starting data export to {output_dir}/')
        )
        
        # Export in JSON format (preserves relationships)
        if export_format in ['json', 'both']:
            self.export_json(output_dir, timestamp)
        
        # Export in CSV format (easier to import into other systems)
        if export_format in ['csv', 'both']:
            self.export_csv(output_dir, timestamp)
        
        self.stdout.write(
            self.style.SUCCESS('✅ Data export completed successfully!')
        )

    def export_json(self, output_dir, timestamp):
        """Export data in JSON format preserving relationships"""
        self.stdout.write('📦 Exporting JSON data...')
        
        # Export each model separately for better organization
        models_to_export = [
            (Country, 'countries'),
            (City, 'cities'), 
            (Category, 'categories'),
            (Business, 'businesses'),
        ]
        
        for model, filename in models_to_export:
            data = serializers.serialize('json', model.objects.all(), indent=2)
            filepath = os.path.join(output_dir, f'{filename}_{timestamp}.json')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(data)
            
            count = model.objects.count()
            self.stdout.write(f'  ✅ {filename}: {count} records → {filepath}')

    def export_csv(self, output_dir, timestamp):
        """Export data in CSV format for easy import"""
        self.stdout.write('📋 Exporting CSV data...')
        
        # Export Countries
        self.export_countries_csv(output_dir, timestamp)
        
        # Export Cities
        self.export_cities_csv(output_dir, timestamp)
        
        # Export Categories
        self.export_categories_csv(output_dir, timestamp)
        
        # Export Businesses (main data)
        self.export_businesses_csv(output_dir, timestamp)

    def export_countries_csv(self, output_dir, timestamp):
        filepath = os.path.join(output_dir, f'countries_{timestamp}.csv')
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'id', 'name', 'code', 'slug', 'is_eu_member', 'is_active'
            ])
            
            for country in Country.objects.all():
                writer.writerow([
                    country.id,
                    country.name,
                    country.code,
                    country.slug,
                    country.is_eu_member,
                    country.is_active
                ])
        
        count = Country.objects.count()
        self.stdout.write(f'  ✅ countries: {count} records → {filepath}')

    def export_cities_csv(self, output_dir, timestamp):
        filepath = os.path.join(output_dir, f'cities_{timestamp}.csv')
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'id', 'name', 'slug', 'country_name', 'country_code',
                'latitude', 'longitude', 'population', 'is_capital'
            ])
            
            for city in City.objects.select_related('country'):
                writer.writerow([
                    city.id,
                    city.name,
                    city.slug,
                    city.country.name,
                    city.country.code,
                    str(city.latitude) if city.latitude else '',
                    str(city.longitude) if city.longitude else '',
                    city.population or '',
                    city.is_capital
                ])
        
        count = City.objects.count()
        self.stdout.write(f'  ✅ cities: {count} records → {filepath}')

    def export_categories_csv(self, output_dir, timestamp):
        filepath = os.path.join(output_dir, f'categories_{timestamp}.csv')
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'id', 'name', 'slug', 'description', 'icon',
                'parent_name', 'is_active', 'sort_order', 'created_at'
            ])
            
            for category in Category.objects.select_related('parent'):
                writer.writerow([
                    category.id,
                    category.name,
                    category.slug,
                    category.description,
                    category.icon,
                    category.parent.name if category.parent else '',
                    category.is_active,
                    category.sort_order,
                    category.created_at.isoformat() if category.created_at else ''
                ])
        
        count = Category.objects.count()
        self.stdout.write(f'  ✅ categories: {count} records → {filepath}')

    def export_businesses_csv(self, output_dir, timestamp):
        """Export the main business data - this is your most valuable data!"""
        filepath = os.path.join(output_dir, f'businesses_{timestamp}.csv')
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'id', 'name', 'slug', 'description', 'short_description',
                'email', 'phone', 'website', 'address', 
                'city_name', 'country_name', 'postal_code',
                'latitude', 'longitude', 'category_name', 
                'plan', 'status', 'featured', 'verified',
                'meta_title', 'meta_description', 'keywords',
                'views_count', 'clicks_count',
                'monday_hours', 'tuesday_hours', 'wednesday_hours',
                'thursday_hours', 'friday_hours', 'saturday_hours', 'sunday_hours',
                'created_at', 'updated_at', 'published_at'
            ])
            
            for business in Business.objects.select_related('city__country', 'category'):
                writer.writerow([
                    str(business.id),
                    business.name,
                    business.slug,
                    business.description,
                    business.short_description,
                    business.email,
                    business.phone,
                    business.website,
                    business.address,
                    business.city.name,
                    business.city.country.name,
                    business.postal_code,
                    str(business.latitude) if business.latitude else '',
                    str(business.longitude) if business.longitude else '',
                    business.category.name,
                    business.plan,
                    business.status,
                    business.featured,
                    business.verified,
                    business.meta_title,
                    business.meta_description,
                    business.keywords,
                    business.views_count,
                    business.clicks_count,
                    business.monday_hours,
                    business.tuesday_hours,
                    business.wednesday_hours,
                    business.thursday_hours,
                    business.friday_hours,
                    business.saturday_hours,
                    business.sunday_hours,
                    business.created_at.isoformat() if business.created_at else '',
                    business.updated_at.isoformat() if business.updated_at else '',
                    business.published_at.isoformat() if business.published_at else ''
                ])
        
        count = Business.objects.count()
        self.stdout.write(f'  ✅ businesses: {count} records → {filepath}')
        
        # Create summary file
        summary_path = os.path.join(output_dir, f'export_summary_{timestamp}.txt')
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(f"ListAcross.eu Data Export Summary\n")
            f.write(f"=====================================\n")
            f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Export Format: CSV + JSON\n\n")
            f.write(f"Records Exported:\n")
            f.write(f"- Countries: {Country.objects.count()}\n")
            f.write(f"- Cities: {City.objects.count()}\n")
            f.write(f"- Categories: {Category.objects.count()}\n")
            f.write(f"- Businesses: {Business.objects.count()}\n\n")
            f.write(f"Key Data Fields Preserved:\n")
            f.write(f"- Complete business information (name, contact, location)\n")
            f.write(f"- Geographic data (coordinates, addresses)\n")
            f.write(f"- Business categorization\n")
            f.write(f"- SEO metadata (titles, descriptions, keywords)\n")
            f.write(f"- Business hours and operational data\n")
            f.write(f"- Statistics (views, clicks)\n")
            f.write(f"- Timestamps for all records\n\n")
            f.write(f"Files Generated:\n")
            f.write(f"- businesses_{timestamp}.csv (main business data)\n")
            f.write(f"- cities_{timestamp}.csv (location data) \n")
            f.write(f"- countries_{timestamp}.csv (country data)\n")
            f.write(f"- categories_{timestamp}.csv (business categories)\n")
            f.write(f"- JSON files for each entity type\n")
        
        self.stdout.write(f'📋 Summary report → {summary_path}')