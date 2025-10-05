# businesses/urls_enhanced.py
"""
Enhanced URL patterns for country/city structure
"""

from django.urls import path
from . import views_country_city

# Enhanced URL patterns
enhanced_urlpatterns = [
    # Countries list
    path('countries/', views_country_city.country_list, name='country_list'),
    
    # Country pages: /portugal/
    path('<slug:country_slug>/', views_country_city.country_businesses, name='country_detail'),
    
    # City pages: /portugal/porto/
    path('<slug:country_slug>/<slug:city_slug>/', views_country_city.city_businesses, name='city_detail'),
]