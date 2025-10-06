# businesses/urls_seo_optimized.py
"""
SEO-Optimized URL patterns for maximum search engine visibility
Designed to compete with Europages.com and dominate local search
"""

from django.urls import path
from . import views_country_city, views_listings, views_seo

# SEO-Optimized URL patterns
seo_optimized_urlpatterns = [
    # Global category pages (high authority)
    path('restaurants/', views_seo.global_category_page, {'category': 'restaurants'}, name='global_restaurants'),
    path('technology/', views_seo.global_category_page, {'category': 'technology'}, name='global_technology'),
    path('retail/', views_seo.global_category_page, {'category': 'retail'}, name='global_retail'),
    path('services/', views_seo.global_category_page, {'category': 'services'}, name='global_services'),
    path('manufacturing/', views_seo.global_category_page, {'category': 'manufacturing'}, name='global_manufacturing'),
    
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
    
    # Country category combinations (/restaurants/portugal/)
    path('<slug:category_slug>/<slug:country_slug>/', views_seo.category_country_businesses, name='category_country'),
    
    # Enhanced country pages with categories (/portugal/restaurants/)
    path('<slug:country_slug>/<slug:category_slug>/', views_seo.country_category_businesses, name='country_category'),
    
    # Countries list (keep existing)
    path('countries/', views_country_city.country_list, name='country_list'),
    
    # City pages: /portugal/porto/ (IMPORTANT: This handles ?category=xxx queries)
    path('<slug:country_slug>/<slug:city_slug>/', views_country_city.city_businesses, name='city_detail'),
    
    # Country pages: /portugal/
    path('<slug:country_slug>/', views_country_city.country_businesses, name='country_detail'),
]