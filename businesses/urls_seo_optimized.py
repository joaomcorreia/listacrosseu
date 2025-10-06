# businesses/urls_seo_optimized.py
"""
SEO-Optimized URL patterns for maximum search engine visibility
Designed to compete with Europages.com and dominate local search
"""

from django.urls import path
from . import views_country_city, views_listings, views_seo, views_smart_routing, views_dynamic_routing

# SEO-Optimized URL patterns
seo_optimized_urlpatterns = [
    # Dynamic single-slug router (handles all categories and countries)
    # This replaces the hardcoded category patterns above
    
    # SEO landing pages (money keywords)
    path('top-restaurants-europe/', views_seo.top_restaurants_europe, name='top_restaurants_europe'),
    path('best-tech-companies-europe/', views_seo.best_tech_companies_europe, name='best_tech_companies_europe'),
    path('european-business-directory/', views_seo.european_business_directory, name='european_business_directory'),
    
    # Individual business with full path (/portugal/porto/restaurants/business-name/) - MOST SPECIFIC FIRST
    path('<slug:country_slug>/<slug:city_slug>/<slug:category_slug>/<slug:business_slug>/', 
         views_seo.business_detail_seo, name='business_detail_seo'),
    
    # City category combinations (/restaurants/portugal/porto/)
    path('<slug:category_slug>/<slug:country_slug>/<slug:city_slug>/', views_seo.category_country_city_businesses, name='category_country_city'),
    
    # Enhanced city pages with categories (/portugal/porto/restaurants/)
    path('<slug:country_slug>/<slug:city_slug>/<slug:category_slug>/', views_seo.city_category_businesses, name='city_category'),
    
    # Pagination for category pages
    path('<slug:category_slug>/<slug:country_slug>/<slug:city_slug>/page/<int:page>/', 
         views_seo.category_country_city_businesses, name='category_country_city_paginated'),
    
    # Countries list (keep existing)
    path('countries/', views_country_city.country_list, name='country_list'),
    
    # Smart router for two-slug patterns (handles both country/city and category/country)
    path('<slug:first_slug>/<slug:second_slug>/', views_smart_routing.smart_two_slug_router, name='smart_two_slug'),
    
    # Dynamic single-slug router (categories vs countries)
    path('<slug:slug>/', views_dynamic_routing.smart_single_slug_router, name='dynamic_single_slug'),
]