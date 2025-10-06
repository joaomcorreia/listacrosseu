# businesses/views_dynamic_routing.py
"""
Dynamic routing for single-slug URLs (categories vs countries)
"""

from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Country, Category
from .views_seo import global_category_page
from .views_country_city import country_businesses


def smart_single_slug_router(request, slug):
    """
    Intelligently route single-slug URLs by checking what they represent
    
    Priority order:
    1. Check if it's a valid category (e.g., /education/, /health/, /finance/)
    2. Check if it's a valid country (e.g., /portugal/, /france/, /spain/)
    3. Return 404 if neither
    """
    
    # First, check if it's a category
    try:
        category = Category.objects.get(slug=slug)
        # It's a valid category - use global_category_page view
        return global_category_page(request, slug)
    except Category.DoesNotExist:
        pass
    
    # Second, check if it's a country
    try:
        country = Country.objects.get(slug=slug, is_active=True)
        # It's a valid country - use country_businesses view
        return country_businesses(request, slug)
    except Country.DoesNotExist:
        pass
    
    # If neither pattern matches, raise 404
    raise Http404("Page not found")