from django.urls import path
from . import views

urlpatterns = [
    path('settings/', views.site_settings, name='site_settings'),
    path('maintenance-status/', views.maintenance_status, name='maintenance_status'),
    path('animation-settings/', views.animation_settings, name='animation_settings'),
]