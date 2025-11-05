from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .api_views import (
    BusinessListAPIView,
    BusinessDetailAPIView,
    BusinessSearchAPIView,
    BusinessStatsAPIView,
    BusinessTranslationAPIView,
    CategoryListAPIView,
    CityListAPIView,
    CountryListAPIView,
    ReviewListCreateAPIView,
    increment_business_clicks,
)

app_name = 'api'

urlpatterns = [
    # Authentication endpoints
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Location endpoints
    path('countries/', CountryListAPIView.as_view(), name='country-list'),
    path('cities/', CityListAPIView.as_view(), name='city-list'),
    
    # Category endpoints
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    
    # Business endpoints
    path('businesses/', BusinessListAPIView.as_view(), name='business-list'),
    path('businesses/<slug:slug>/', BusinessDetailAPIView.as_view(), name='business-detail'),
    path('businesses/<int:business_id>/click/', increment_business_clicks, name='business-click'),
    path('businesses/<int:business_id>/reviews/', ReviewListCreateAPIView.as_view(), name='business-reviews'),
    
    # Search endpoints
    path('search/', BusinessSearchAPIView.as_view(), name='business-search'),
    
    # Stats endpoints
    path('stats/', BusinessStatsAPIView.as_view(), name='business-stats'),
    
    # Translation endpoints (for 27 EU languages)
    path('businesses/<int:business_id>/translations/<str:language_code>/', 
         BusinessTranslationAPIView.as_view(), name='business-translation'),
]