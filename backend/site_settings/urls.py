from django.urls import path
from .views import SiteSettingView, LogoView, FaviconView

urlpatterns = [
    path('', SiteSettingView.as_view(), name='site-settings'),
    path('logo/', LogoView.as_view(), name='site-logo'),
    path('favicon/', FaviconView.as_view(), name='site-favicon'),
]