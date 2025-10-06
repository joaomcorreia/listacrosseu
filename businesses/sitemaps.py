from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from .models import Country, City, Business, Category

class HomepageSitemap(Sitemap):
    """Homepage sitemap"""
    priority = 1.0
    changefreq = 'daily'
    
    def items(self):
        return ['homepage']
    
    def location(self, item):
        return reverse('homepage')
    
    def lastmod(self, obj):
        return timezone.now()

class CountrySitemap(Sitemap):
    """Country pages sitemap"""
    changefreq = "weekly"
    priority = 0.9
    
    def items(self):
        return Country.objects.filter(is_active=True).order_by('name')
    
    def location(self, obj):
        return f'/{obj.slug}/'
    
    def lastmod(self, obj):
        # Get the latest business update in this country
        latest_business = Business.objects.filter(
            city__country=obj, 
            status='active'
        ).order_by('-updated_at').first()
        return latest_business.updated_at if latest_business else obj.updated_at

class CitySitemap(Sitemap):
    """City pages sitemap"""
    changefreq = "weekly" 
    priority = 0.8
    
    def items(self):
        return City.objects.select_related('country').filter(
            country__is_active=True
        ).order_by('country__name', 'name')
    
    def location(self, obj):
        return f'/{obj.country.slug}/{obj.slug}/'
    
    def lastmod(self, obj):
        # Get the latest business update in this city
        latest_business = Business.objects.filter(
            city=obj, 
            status='active'
        ).order_by('-updated_at').first()
        return latest_business.updated_at if latest_business else obj.updated_at

class CategorySitemap(Sitemap):
    """Category pages sitemap"""
    changefreq = "weekly"
    priority = 0.7
    
    def items(self):
        return Category.objects.filter(is_active=True).order_by('name')
    
    def location(self, obj):
        return f'/category/{obj.slug}/'
    
    def lastmod(self, obj):
        return obj.updated_at

class BusinessSitemap(Sitemap):
    """Business detail pages sitemap - SEO optimized URLs"""
    changefreq = "monthly"
    priority = 0.6
    limit = 5000  # Limit for performance
    
    def items(self):
        return Business.objects.select_related('city', 'city__country', 'category').filter(
            status='active'
        ).order_by('-updated_at')[:self.limit]
    
    def location(self, obj):
        return f'/{obj.city.country.slug}/{obj.city.slug}/{obj.category.slug}/{obj.slug}/'
    
    def lastmod(self, obj):
        return obj.updated_at

class CategoryCountrySitemap(Sitemap):
    """Category + Country combination pages (/restaurants/portugal/)"""
    changefreq = "daily"
    priority = 0.8
    
    def items(self):
        combinations = []
        for category in Category.objects.filter(is_active=True):
            for country in Country.objects.filter(is_active=True):
                if Business.objects.filter(category=category, city__country=country, status='active').exists():
                    combinations.append((category, country))
        return combinations
    
    def location(self, obj):
        category, country = obj
        return f'/{category.slug}/{country.slug}/'

class CategoryCountryCitySitemap(Sitemap):
    """Category + Country + City combination pages (/restaurants/portugal/porto/)"""
    changefreq = "weekly"
    priority = 0.7
    
    def items(self):
        combinations = []
        for category in Category.objects.filter(is_active=True):
            for city in City.objects.select_related('country').all():
                if Business.objects.filter(category=category, city=city, status='active').exists():
                    combinations.append((category, city.country, city))
        return combinations[:2000]  # Limit for performance
    
    def location(self, obj):
        category, country, city = obj
        return f'/{category.slug}/{country.slug}/{city.slug}/'

class CountryCategorySitemap(Sitemap):
    """Country + Category combination pages (/portugal/restaurants/)"""
    changefreq = "weekly"
    priority = 0.7
    
    def items(self):
        combinations = []
        for country in Country.objects.filter(is_active=True):
            for category in Category.objects.filter(is_active=True):
                if Business.objects.filter(city__country=country, category=category, status='active').exists():
                    combinations.append((country, category))
        return combinations
    
    def location(self, obj):
        country, category = obj
        return f'/{country.slug}/{category.slug}/'

class GlobalCategorySitemap(Sitemap):
    """Global category pages (/restaurants/, /technology/, etc.)"""
    changefreq = "daily"
    priority = 0.9
    
    def items(self):
        return Category.objects.filter(is_active=True).order_by('name')
    
    def location(self, obj):
        return f'/{obj.slug}/'

class StaticPagesSitemap(Sitemap):
    """Static pages sitemap"""
    changefreq = "monthly"
    priority = 0.5
    
    def items(self):
        return [
            'register_business',
            'data_sources',
            'pricing_plans',
            'success_stories',
        ]
    
    def location(self, item):
        return reverse(item)
    
    def lastmod(self, obj):
        return timezone.now()

# Enhanced sitemap dictionary for SEO optimization
sitemaps = {
    'homepage': HomepageSitemap,
    'countries': CountrySitemap,
    'cities': CitySitemap,
    'categories': CategorySitemap,
    'businesses': BusinessSitemap,
    'static': StaticPagesSitemap,
    # SEO-Optimized combination pages
    'global_categories': GlobalCategorySitemap,
    'category_countries': CategoryCountrySitemap,
    'category_country_cities': CategoryCountryCitySitemap,
    'country_categories': CountryCategorySitemap,
}