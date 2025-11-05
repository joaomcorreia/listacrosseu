from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('businesses/', views.BusinessListView.as_view(), name='business-list'),
    path('businesses/search/', views.business_search, name='business-search'),
    path('businesses/<slug:slug>/', views.BusinessDetailView.as_view(), name='business-detail'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('search/businesses/', views.BusinessSearchView.as_view(), name='search-businesses'),
    
    # CSV Upload URLs
    path('csv-upload/', views.csv_upload_view, name='csv_upload'),
    path('api/csv-upload/', views.CSVUploadAPIView.as_view(), name='api-csv-upload'),
    path('api/csv-upload/<int:upload_id>/status/', views.csv_upload_status, name='csv-upload-status'),
    path('api/csv-upload/<int:upload_id>/progress/', views.csv_upload_progress, name='csv-upload-progress'),
    
    # Directory API URLs
    path('countries/', views.countries_list, name='countries-list'),
    path('cities/', views.cities_list, name='cities-list'),
    path('categories/counts/', views.categories_with_counts, name='categories-with-counts'),
    path('countries/<str:country>/businesses/', views.businesses_by_country, name='businesses-by-country'),
]