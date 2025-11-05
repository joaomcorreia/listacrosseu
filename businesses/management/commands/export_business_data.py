"""
Django Management Command for Data Export
Usage: python manage.py export_business_data
"""
from django.core.management.base import BaseCommand
from django.http import HttpResponse
import csv
import os
from datetime import datetime
from businesses.models import Business, Country, City, Category
from django.db.models import Count

class Command(BaseCommand):
    help = 'Export business data to CSV files for review'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--format',
            type=str,
            default='all',
            help='Export format: all, summary, countries, issues'
        )
        parser.add_argument(
            '--country',
            type=str,
            help='Export specific country only'
        )
    
    def handle(self, *args, **options):
        """Handle the export command"""
        
        self.stdout.write(
            self.style.SUCCESS('📦 Starting business data export...')
        )
        
        export_format = options['format']
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if export_format == 'all' or export_format == 'summary':
            self.export_summary(timestamp)
        
        if export_format == 'all' or export_format == 'countries':
            self.export_by_countries(timestamp, options.get('country'))
        
        if export_format == 'all' or export_format == 'issues':
            self.export_issues(timestamp)
        
        if export_format == 'all':
            self.export_all_businesses(timestamp)
        
        self.stdout.write(
            self.style.SUCCESS('✅ Export completed successfully!')
        )
    
    def export_summary(self, timestamp):
        """Export summary statistics"""
        filename = f"business_summary_{timestamp}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Metric', 'Count', 'Percentage'])
            
            total = Business.objects.count()
            writer.writerow(['Total Businesses', total, '100%'])
            writer.writerow(['', '', ''])  # Empty row
            
            # By country
            writer.writerow(['BY COUNTRY', '', ''])
            countries = Business.objects.select_related('city__country').values(
                'city__country__name'
            ).annotate(count=Count('id')).order_by('-count')
            
            for country in countries:
                percentage = f"{(country['count']/total*100):.1f}%"
                writer.writerow([country['city__country__name'], country['count'], percentage])
            
            writer.writerow(['', '', ''])  # Empty row
            
            # By city (top 10)
            writer.writerow(['TOP CITIES', '', ''])
            cities = Business.objects.values('city__name', 'city__country__name').annotate(
                count=Count('id')
            ).order_by('-count')[:10]
            
            for city in cities:
                city_name = f"{city['city__name']}, {city['city__country__name']}"
                percentage = f"{(city['count']/total*100):.1f}%"
                writer.writerow([city_name, city['count'], percentage])
        
        self.stdout.write(f"📊 Summary exported to: {filename}")
    
    def export_by_countries(self, timestamp, specific_country=None):
        """Export businesses by country"""
        
        if specific_country:
            countries = Country.objects.filter(slug=specific_country)
        else:
            countries = Country.objects.filter(
                cities__businesses__isnull=False
            ).distinct()
        
        for country in countries:
            filename = f"businesses_{country.slug}_{timestamp}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'Name', 'Category', 'City', 'Address', 'Phone', 
                    'Email', 'Website', 'Verified', 'Status'
                ]
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                businesses = Business.objects.filter(
                    city__country=country
                ).select_related('category', 'city').order_by('city__name', 'name')
                
                for business in businesses:
                    writer.writerow({
                        'Name': business.name,
                        'Category': business.category.name if business.category else 'Uncategorized',
                        'City': business.city.name,
                        'Address': business.address or '',
                        'Phone': business.phone or '',
                        'Email': business.email or '',
                        'Website': business.website or '',
                        'Verified': 'Yes' if business.verified else 'No',
                        'Status': business.status.title()
                    })
            
            count = businesses.count()
            self.stdout.write(f"📄 {country.name}: {count} businesses exported to {filename}")
    
    def export_issues(self, timestamp):
        """Export potential data quality issues"""
        filename = f"data_issues_{timestamp}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Business Name', 'Country', 'City', 'Issue', 'Details']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            issues_found = 0
            
            for business in Business.objects.select_related('city__country').all():
                # Check for missing contact info
                if not business.phone and not business.website and not business.email:
                    writer.writerow({
                        'Business Name': business.name,
                        'Country': business.city.country.name if business.city else '',
                        'City': business.city.name if business.city else '',
                        'Issue': 'No Contact Information',
                        'Details': 'Missing phone, email, and website'
                    })
                    issues_found += 1
                
                # Check for missing address
                if not business.address:
                    writer.writerow({
                        'Business Name': business.name,
                        'Country': business.city.country.name if business.city else '',
                        'City': business.city.name if business.city else '',
                        'Issue': 'Missing Address',
                        'Details': 'No address provided'
                    })
                    issues_found += 1
                
                # Check for very short descriptions
                if business.description and len(business.description.strip()) < 10:
                    writer.writerow({
                        'Business Name': business.name,
                        'Country': business.city.country.name if business.city else '',
                        'City': business.city.name if business.city else '',
                        'Issue': 'Poor Description',
                        'Details': f'Description too short: "{business.description[:50]}..."'
                    })
                    issues_found += 1
        
        self.stdout.write(f"⚠️  Issues exported to: {filename} ({issues_found} issues found)")
    
    def export_all_businesses(self, timestamp):
        """Export all businesses to single file"""
        filename = f"all_businesses_{timestamp}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'ID', 'Name', 'Category', 'Country', 'City', 'Address', 
                'Phone', 'Email', 'Website', 'Description', 'Verified', 
                'Status', 'Created'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            businesses = Business.objects.select_related(
                'category', 'city__country'
            ).order_by('city__country__name', 'city__name', 'name')
            
            for business in businesses:
                writer.writerow({
                    'ID': business.id,
                    'Name': business.name,
                    'Category': business.category.name if business.category else '',
                    'Country': business.city.country.name if business.city else '',
                    'City': business.city.name if business.city else '',
                    'Address': business.address or '',
                    'Phone': business.phone or '',
                    'Email': business.email or '',
                    'Website': business.website or '',
                    'Description': (business.description or '')[:100] + '...' if business.description and len(business.description) > 100 else business.description or '',
                    'Verified': 'Yes' if business.verified else 'No',
                    'Status': business.status.title(),
                    'Created': business.created_at.strftime('%Y-%m-%d') if business.created_at else ''
                })
        
        count = Business.objects.count()
        self.stdout.write(f"📄 All businesses exported to: {filename} ({count:,} businesses)")