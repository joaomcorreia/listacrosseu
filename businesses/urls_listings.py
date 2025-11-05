"""
URLs for Business Listings
"""

from django.urls import path
from . import views_listings, views_porto

# Listing URLs
listing_urlpatterns = [
    # Business listings
    path('businesses/', views_listings.business_list, name='business_list'),
    path('business/<slug:slug>/', views_listings.business_detail, name='business_detail'),
    
    # Listings by location
    path('cities/', views_listings.city_list, name='city_list'),
    path('city/<slug:city_slug>/', views_listings.businesses_by_city, name='businesses_by_city'),
    
    # Listings by category
    path('category/<slug:category_slug>/', views_listings.businesses_by_category, name='businesses_by_category'),
    
    # Special Porto page
    path('porto/', views_porto.porto_businesses, name='porto_businesses'),
]