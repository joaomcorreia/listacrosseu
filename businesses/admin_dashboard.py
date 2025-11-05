from django.contrib import admin
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import path
from django.db.models import Count
from businesses.models import Business, Category, Country, City


class CustomAdminSite(admin.AdminSite):
    site_header = "List Across EU - Business Directory Admin"
    site_title = "List Across EU Admin"
    index_title = "Business Directory Management"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('business-stats/', self.admin_view(self.business_stats_view), name='business_stats'),
        ]
        return custom_urls + urls
    
    def business_stats_view(self, request):
        """Custom view showing business statistics"""
        
        # Overall stats
        total_businesses = Business.objects.count()
        total_countries = Country.objects.count()
        total_cities = City.objects.count()
        total_categories = Category.objects.count()
        
        # Active stats (with businesses)
        countries_with_businesses = Country.objects.filter(cities__businesses__isnull=False).distinct().count()
        cities_with_businesses = City.objects.filter(businesses__isnull=False).count()
        categories_with_businesses = Category.objects.filter(businesses__isnull=False).count()
        
        # Top countries by business count
        top_countries = Country.objects.annotate(
            business_count=Count('cities__businesses')
        ).filter(business_count__gt=0).order_by('-business_count')[:10]
        
        # Top cities by business count
        top_cities = City.objects.annotate(
            business_count=Count('businesses')
        ).filter(business_count__gt=0).order_by('-business_count')[:15]
        
        # Top categories by business count
        top_categories = Category.objects.annotate(
            business_count=Count('businesses')
        ).filter(business_count__gt=0).order_by('-business_count')[:15]
        
        # Empty categories (need attention)
        empty_categories = Category.objects.filter(businesses__isnull=True).order_by('name')[:20]
        
        # Empty countries (need attention)
        empty_countries = Country.objects.filter(cities__businesses__isnull=True).distinct().order_by('name')
        
        context = {
            'title': 'Business Statistics Dashboard',
            'total_businesses': total_businesses,
            'total_countries': total_countries,
            'total_cities': total_cities,
            'total_categories': total_categories,
            'countries_with_businesses': countries_with_businesses,
            'cities_with_businesses': cities_with_businesses,
            'categories_with_businesses': categories_with_businesses,
            'top_countries': top_countries,
            'top_cities': top_cities,
            'top_categories': top_categories,
            'empty_categories': empty_categories,
            'empty_countries': empty_countries,
            'coverage_percentage': {
                'countries': round((countries_with_businesses / total_countries) * 100, 1) if total_countries > 0 else 0,
                'cities': round((cities_with_businesses / total_cities) * 100, 1) if total_cities > 0 else 0,
                'categories': round((categories_with_businesses / total_categories) * 100, 1) if total_categories > 0 else 0,
            }
        }
        
        return TemplateResponse(request, 'admin/business_stats.html', context)

# Replace default admin site
admin.site = CustomAdminSite()