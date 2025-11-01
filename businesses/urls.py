from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views_admin import data_overview
from .urls_registration import registration_urlpatterns
from .urls_listings import listing_urlpatterns
from .urls_seo_optimized import seo_optimized_urlpatterns
from .listy_api import ListyAssistantView

router = DefaultRouter()
router.register(r'businesses', views.BusinessViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'countries', views.CountryViewSet)
router.register(r'cities', views.CityViewSet)
router.register(r'reviews', views.ReviewViewSet)

urlpatterns = [
    # API routes
    path('api/', include(router.urls)),
    path('api/businesses/stats/', views.BusinessViewSet.stats, name='business_stats'),
    path('api/businesses/countries/', views.BusinessViewSet.countries, name='business_countries'),
    path('api/businesses/cities/', views.BusinessViewSet.cities, name='business_cities'),
    path('api/businesses/categories/', views.BusinessViewSet.categories, name='business_categories'),
    path('api/search/', views.BusinessSearchView.as_view(), name='business_search'),
    path('api/featured/', views.FeaturedBusinessesView.as_view(), name='featured_businesses'),
    
    # Listy AI Assistant API
    path('api/listy/', ListyAssistantView.as_view(), name='listy_assistant'),
    
    # Admin/Debug routes
    path('admin/data-overview/', data_overview, name='data_overview'),
    
    # Registration system routes (includes homepage) - MUST BE FIRST
    *registration_urlpatterns,
    
    # Business listings (keep for backward compatibility)
    *listing_urlpatterns,
    
    # SEO-Optimized URLs - MUST BE LAST (catch-all patterns)
    *seo_optimized_urlpatterns,
]