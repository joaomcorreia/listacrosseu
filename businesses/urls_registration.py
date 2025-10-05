"""
URLs for Business Registration System
"""

from django.urls import path
from . import views_registration
from .views_data_sources import data_sources

# Registration URLs
registration_urlpatterns = [
    # Business Registration
    path('register/', views_registration.register_business, name='register_business'),
    path('verify/<uuid:registration_id>/', views_registration.verify_registration, name='verify_registration'),
    path('status/<uuid:registration_id>/', views_registration.registration_status, name='registration_status'),
    path('resend/<uuid:registration_id>/', views_registration.resend_verification, name='resend_verification'),
    
    # Business Claims
    path('claim/<int:business_id>/', views_registration.business_claim, name='business_claim'),
    
    # Marketing Pages
    path('success-stories/', views_registration.business_success_stories, name='success_stories'),
    path('pricing/', views_registration.pricing_plans, name='pricing_plans'),
    
    # Data Sources & Transparency
    path('data-sources/', data_sources, name='data_sources'),
    
    # Enhanced Homepage
    path('', views_registration.homepage, name='homepage'),
]