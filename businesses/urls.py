from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .urls_registration import registration_urlpatterns
from .urls_listings import listing_urlpatterns
from .urls_enhanced import enhanced_urlpatterns

router = DefaultRouter()
router.register(r'businesses', views.BusinessViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'countries', views.CountryViewSet)
router.register(r'cities', views.CityViewSet)
router.register(r'reviews', views.ReviewViewSet)

urlpatterns = [
    # API routes
    path('api/', include(router.urls)),
    path('api/search/', views.BusinessSearchView.as_view(), name='business_search'),
    path('api/featured/', views.FeaturedBusinessesView.as_view(), name='featured_businesses'),
    
    # Registration system routes (includes homepage) - MUST BE FIRST
    *registration_urlpatterns,
    
    # Business listings
    *listing_urlpatterns,
    
    # Enhanced country/city URLs - MUST BE LAST (catch-all patterns)
    *enhanced_urlpatterns,
]