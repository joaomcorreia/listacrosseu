from django.urls import path
from . import views

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
]