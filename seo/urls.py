from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SeoCustomDashboardView, CountryViewSet, LanguageViewSet, 
    SeoPlanViewSet, SeoPageViewSet, SeoContentBlockViewSet
)

# API Router for DRF endpoints
router = DefaultRouter()
router.register(r'countries', CountryViewSet)
router.register(r'languages', LanguageViewSet)  
router.register(r'plans', SeoPlanViewSet)
router.register(r'pages', SeoPageViewSet)
router.register(r'content-blocks', SeoContentBlockViewSet, basename='seocontentblock')

app_name = 'seo'

urlpatterns = [
    # Custom admin dashboard
    path('dashboard/', SeoCustomDashboardView.as_view(), name='dashboard'),
    
    # API endpoints
    path('api/', include(router.urls)),
]