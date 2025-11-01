from django.core.management.base import BaseCommand
from django.db import transaction
from catalog.models import Category, Business, BusinessCategory
from geo.models import Country, City, Town
from counters.models import CategoryCountry, CategoryCountryCity, CategoryCityTown, CounterRebuildLog


class Command(BaseCommand):
    help = 'Rebuild all counter tables from scratch'

    def add_arguments(self, parser):
        parser.add_argument(
            '--category',
            type=str,
            help='Rebuild counters for specific category slug only'
        )

    def handle(self, *args, **options):
        category_slug = options.get('category')
        
        if category_slug:
            self.rebuild_category_counters(category_slug)
        else:
            self.rebuild_all_counters()

    @transaction.atomic
    def rebuild_all_counters(self):
        """Rebuild all counter tables"""
        self.stdout.write('Rebuilding all counter tables...')
        
        # Clear existing counters
        self.stdout.write('Clearing existing counters...')
        CategoryCountry.objects.all().delete()
        CategoryCountryCity.objects.all().delete()
        CategoryCityTown.objects.all().delete()
        
        # Rebuild each counter table
        self._rebuild_category_country_counters()
        self._rebuild_category_country_city_counters()
        self._rebuild_category_city_town_counters()
        
        # Log the rebuild
        CounterRebuildLog.objects.create(
            rebuild_type='full',
            notes='All counter tables rebuilt'
        )
        
        self.stdout.write(self.style.SUCCESS('All counters rebuilt successfully'))

    @transaction.atomic
    def rebuild_category_counters(self, category_slug):
        """Rebuild counters for a specific category"""
        try:
            category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            self.stderr.write(f'Category not found: {category_slug}')
            return
        
        self.stdout.write(f'Rebuilding counters for category: {category_slug}')
        
        # Clear existing counters for this category
        CategoryCountry.objects.filter(category=category).delete()
        CategoryCountryCity.objects.filter(category=category).delete()
        CategoryCityTown.objects.filter(category=category).delete()
        
        # Rebuild counters for this category
        self._rebuild_category_country_counters(category)
        self._rebuild_category_country_city_counters(category)
        self._rebuild_category_city_town_counters(category)
        
        # Log the rebuild
        CounterRebuildLog.objects.create(
            rebuild_type='category',
            notes=f'Counters rebuilt for category: {category_slug}'
        )
        
        self.stdout.write(self.style.SUCCESS(f'Counters for {category_slug} rebuilt successfully'))

    def _rebuild_category_country_counters(self, specific_category=None):
        """Rebuild CategoryCountry counters"""
        self.stdout.write('Rebuilding category-country counters...')
        
        # Base query for active businesses
        base_query = """
        INSERT INTO counters_categorycountry (category_id, country_id, business_count)
        SELECT 
            bc.category_id,
            b.country_id,
            COUNT(*) as business_count
        FROM catalog_businesscategory bc
        JOIN catalog_business b ON bc.business_id = b.id
        WHERE b.status = 'active'
        """
        
        if specific_category:
            base_query += f" AND bc.category_id = {specific_category.id}"
        
        base_query += """
        GROUP BY bc.category_id, b.country_id
        HAVING COUNT(*) > 0
        """
        
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(base_query)
        
        count = CategoryCountry.objects.count()
        self.stdout.write(f'Created {count} category-country counter records')

    def _rebuild_category_country_city_counters(self, specific_category=None):
        """Rebuild CategoryCountryCity counters"""
        self.stdout.write('Rebuilding category-country-city counters...')
        
        base_query = """
        INSERT INTO counters_categorycountrycity (category_id, country_id, city_id, business_count)
        SELECT 
            bc.category_id,
            b.country_id,
            b.city_id,
            COUNT(*) as business_count
        FROM catalog_businesscategory bc
        JOIN catalog_business b ON bc.business_id = b.id
        WHERE b.status = 'active'
        """
        
        if specific_category:
            base_query += f" AND bc.category_id = {specific_category.id}"
        
        base_query += """
        GROUP BY bc.category_id, b.country_id, b.city_id
        HAVING COUNT(*) > 0
        """
        
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(base_query)
        
        count = CategoryCountryCity.objects.count()
        self.stdout.write(f'Created {count} category-country-city counter records')

    def _rebuild_category_city_town_counters(self, specific_category=None):
        """Rebuild CategoryCityTown counters"""
        self.stdout.write('Rebuilding category-city-town counters...')
        
        base_query = """
        INSERT INTO counters_categorycitytown (category_id, city_id, town_id, business_count)
        SELECT 
            bc.category_id,
            b.city_id,
            b.town_id,
            COUNT(*) as business_count
        FROM catalog_businesscategory bc
        JOIN catalog_business b ON bc.business_id = b.id
        WHERE b.status = 'active' AND b.town_id IS NOT NULL
        """
        
        if specific_category:
            base_query += f" AND bc.category_id = {specific_category.id}"
        
        base_query += """
        GROUP BY bc.category_id, b.city_id, b.town_id
        HAVING COUNT(*) > 0
        """
        
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(base_query)
        
        count = CategoryCityTown.objects.count()
        self.stdout.write(f'Created {count} category-city-town counter records')