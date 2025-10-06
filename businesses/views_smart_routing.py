# businesses/views_smart_routing.py
"""
Smart routing view that can distinguish between different URL patterns
"""

from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Country, City, Category, Business
from .views_country_city import city_businesses
from .views_seo import category_country_businesses


def smart_two_slug_router(request, first_slug, second_slug):
    """
    Intelligently route URLs with two slugs by checking what they represent
    
    Possible interpretations:
    1. country/city (e.g., /belgium/antwerp/)
    2. category/country (e.g., /technology/belgium/)
    """
    
    # First, check if it's a country/city combination
    try:
        country = Country.objects.get(slug=first_slug, is_active=True)
        city = City.objects.get(slug=second_slug, country=country)
        # It's a valid country/city - use city_businesses view
        return city_businesses(request, first_slug, second_slug)
    except (Country.DoesNotExist, City.DoesNotExist):
        pass
    
    # Second, check if it's a category/country combination
    try:
        category = Category.objects.get(slug=first_slug)
        country = Country.objects.get(slug=second_slug, is_active=True)
        # It's a valid category/country - use category_country_businesses view
        return category_country_businesses(request, first_slug, second_slug)
    except (Category.DoesNotExist, Country.DoesNotExist):
        pass
    
    # If neither pattern matches, raise 404
    raise Http404("Page not found")