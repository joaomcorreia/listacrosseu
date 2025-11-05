"""
Duplicate Detection Management Command
Detects and manages duplicate businesses in the admin interface
"""

from django.core.management.base import BaseCommand
from django.db.models import Count
from businesses.models import Business, City
from collections import defaultdict
import json

class Command(BaseCommand):
    help = 'Detect and analyze duplicate businesses'

    def add_arguments(self, parser):
        parser.add_argument(
            '--format',
            choices=['summary', 'detailed', 'json'],
            default='summary',
            help='Output format for duplicate report'
        )
        parser.add_argument(
            '--city',
            type=str,
            help='Filter duplicates by city name'
        )
        parser.add_argument(
            '--country',
            type=str,
            help='Filter duplicates by country code (e.g., DE, ES, FR)'
        )
        parser.add_argument(
            '--threshold',
            type=int,
            default=2,
            help='Minimum number of duplicates to report (default: 2)'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 DUPLICATE DETECTION REPORT'))
        self.stdout.write('=' * 60)
        
        # Build query filters
        filters = {}
        if options['city']:
            filters['city__name__icontains'] = options['city']
        if options['country']:
            filters['city__country__code'] = options['country'].upper()
        
        # Find duplicates
        duplicates = self.find_duplicates(filters, options['threshold'])
        
        # Generate report based on format
        if options['format'] == 'json':
            self.output_json(duplicates)
        elif options['format'] == 'detailed':
            self.output_detailed(duplicates)
        else:
            self.output_summary(duplicates)

    def find_duplicates(self, filters, threshold):
        """Find duplicate businesses based on name, city, and address"""
        
        # Find exact duplicates (same name, city, address)
        exact_duplicates = Business.objects.filter(**filters).values(
            'name', 'city', 'address'
        ).annotate(
            count=Count('id')
        ).filter(count__gte=threshold).order_by('-count')
        
        # Find name duplicates in same city
        name_duplicates = Business.objects.filter(**filters).values(
            'name', 'city'
        ).annotate(
            count=Count('id')
        ).filter(count__gte=threshold).order_by('-count')
        
        # Find potential address duplicates
        address_duplicates = Business.objects.filter(**filters).exclude(
            address__isnull=True
        ).exclude(address='').values(
            'address', 'city'
        ).annotate(
            count=Count('id')
        ).filter(count__gte=threshold).order_by('-count')
        
        return {
            'exact': exact_duplicates,
            'name': name_duplicates,
            'address': address_duplicates
        }

    def output_summary(self, duplicates):
        """Output summary format"""
        
        self.stdout.write(f"\n📊 DUPLICATE SUMMARY:")
        self.stdout.write(f"   Exact duplicates: {duplicates['exact'].count()}")
        self.stdout.write(f"   Name duplicates: {duplicates['name'].count()}")
        self.stdout.write(f"   Address duplicates: {duplicates['address'].count()}")
        
        # Top 10 exact duplicates
        if duplicates['exact'].exists():
            self.stdout.write(f"\n🚨 TOP EXACT DUPLICATES:")
            for i, dup in enumerate(duplicates['exact'][:10], 1):
                try:
                    city = City.objects.get(id=dup['city'])
                    self.stdout.write(
                        f"   {i}. '{dup['name']}' in {city.name}: {dup['count']} times"
                    )
                except City.DoesNotExist:
                    self.stdout.write(
                        f"   {i}. '{dup['name']}': {dup['count']} times (unknown city)"
                    )

    def output_detailed(self, duplicates):
        """Output detailed format with business IDs"""
        
        self.output_summary(duplicates)
        
        self.stdout.write(f"\n📋 DETAILED DUPLICATE ANALYSIS:")
        
        for i, dup in enumerate(duplicates['exact'][:5], 1):
            try:
                city = City.objects.get(id=dup['city'])
                businesses = Business.objects.filter(
                    name=dup['name'],
                    city=city,
                    address=dup['address']
                ).order_by('created_at')
                
                self.stdout.write(f"\n{i}. '{dup['name']}' in {city.name}")
                self.stdout.write(f"   Address: {dup['address']}")
                self.stdout.write(f"   Count: {dup['count']}")
                self.stdout.write(f"   Business IDs:")
                
                for j, business in enumerate(businesses):
                    status = "🟢 KEEP" if j == 0 else "🔴 REMOVE"
                    created = business.created_at.strftime('%Y-%m-%d %H:%M')
                    self.stdout.write(f"     {status} {business.id} (created: {created})")
                    
            except City.DoesNotExist:
                self.stdout.write(f"{i}. Error processing duplicate")

    def output_json(self, duplicates):
        """Output JSON format for programmatic use"""
        
        result = {
            'summary': {
                'exact_count': duplicates['exact'].count(),
                'name_count': duplicates['name'].count(),
                'address_count': duplicates['address'].count()
            },
            'duplicates': []
        }
        
        for dup in duplicates['exact']:
            try:
                city = City.objects.get(id=dup['city'])
                businesses = Business.objects.filter(
                    name=dup['name'],
                    city=city,
                    address=dup['address']
                ).values('id', 'created_at')
                
                result['duplicates'].append({
                    'name': dup['name'],
                    'city': city.name,
                    'country': city.country.name,
                    'address': dup['address'],
                    'count': dup['count'],
                    'business_ids': list(businesses)
                })
            except City.DoesNotExist:
                continue
        
        self.stdout.write(json.dumps(result, indent=2, default=str))