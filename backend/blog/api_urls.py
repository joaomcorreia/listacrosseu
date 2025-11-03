from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import BlogPostViewSet, BlogCategoryViewSet, PricingPlanViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'posts', BlogPostViewSet, basename='blogpost')
router.register(r'categories', BlogCategoryViewSet, basename='blogcategory') 
router.register(r'pricing', PricingPlanViewSet, basename='pricingplan')

app_name = 'blog_api'

urlpatterns = [
    path('v2/', include(router.urls)),
]