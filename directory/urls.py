from django.urls import path
from . import views

urlpatterns = [
    # Main directory views
    path('', views.HomeView.as_view(), name='home'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('country/<str:country_code>/', views.CountryView.as_view(), name='country_detail'),
    path('city/<str:city_name>/', views.CityView.as_view(), name='city_detail'),
    path('business/<slug:slug>/', views.BusinessDetailView.as_view(), name='business_detail'),
    path('search/', views.SearchView.as_view(), name='search'),
    
    # User website views - commented out (websites app moved to dev_archive)
    # path('website/', views.WebsiteView.as_view(), name='user_website'),
    
    # API endpoints
    path('api/businesses/', views.BusinessListAPIView.as_view(), name='api_business_list'),
    path('api/search/', views.SearchAPIView.as_view(), name='api_search'),
]