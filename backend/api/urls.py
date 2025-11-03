from django.urls import path, include
from . import views
from blog.views import blog_posts_api, blog_categories_api, blog_post_detail_api
from blog.pricing_views import pricing_plans_api

urlpatterns = [
    path('categories/', views.categories_list, name='categories_list'),
    path('categories/<slug:category_slug>/countries/', views.category_countries, name='category_countries'),
    path('categories/<slug:category_slug>/countries/<str:country_code>/cities/', views.category_country_cities, name='category_country_cities'),
    path('categories/<slug:category_slug>/countries/<str:country_code>/cities/<slug:city_slug>/towns/', views.category_city_towns, name='category_city_towns'),
    path('countries/', views.countries_list, name='countries_list'),
    path('cities/', views.cities_list, name='cities_list'),
    path('towns/', views.towns_list, name='towns_list'),
    path('businesses/', views.businesses_list, name='businesses_list'),
    path('search/', views.search, name='search'),
    # Blog API endpoints (legacy)
    path('blog/posts/', blog_posts_api, name='blog_posts_api'),
    path('blog/categories/', blog_categories_api, name='blog_categories_api'),
    path('blog/posts/<slug:slug>/', blog_post_detail_api, name='blog_post_detail_api'),
    # Pricing API endpoints (legacy)
    path('pricing/', pricing_plans_api, name='pricing_plans_api'),
    # Advanced Blog API (v2)
    path('blog/', include('blog.api_urls', namespace='blog_api')),
]