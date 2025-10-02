#!/usr/bin/env python
import os
import sys
import django
from django.core.management import execute_from_command_line
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listacrosseu.settings')
django.setup()

# Import models after Django setup
from subscriptions.models import SubscriptionPlan
from businesses.models import Category, Country
from accounts.models import CustomUser

def create_initial_data():
    """Create initial subscription plans and sample data"""
    
    print("Creating subscription plans...")
    
    # Create subscription plans
    plans_data = [
        {
            'name': 'Free Plan',
            'plan_type': 'free',
            'description': 'Basic listing with limited features',
            'monthly_price': 0.00,
            'yearly_price': 0.00,
            'max_listings': 1,
            'can_create_website': False,
            'can_choose_domain': False,
            'can_upload_logo': False,
            'sort_order': 1
        },
        {
            'name': 'Local Plan',
            'plan_type': 'local',
            'description': 'Enhanced local visibility with premium features',
            'monthly_price': 29.00,
            'yearly_price': 290.00,
            'max_listings': 5,
            'can_create_website': False,
            'can_choose_domain': False,
            'can_upload_logo': True,
            'featured_listings': True,
            'analytics_access': True,
            'sort_order': 2
        },
        {
            'name': 'Country Plan',
            'plan_type': 'country',
            'description': 'Country-wide visibility with advanced features',
            'monthly_price': 79.00,
            'yearly_price': 790.00,
            'max_listings': 0,  # Unlimited
            'can_create_website': False,
            'can_choose_domain': False,
            'can_upload_logo': True,
            'featured_listings': True,
            'analytics_access': True,
            'priority_support': True,
            'api_access': True,
            'sort_order': 3
        },
        {
            'name': 'EU Plan',
            'plan_type': 'eu',
            'description': 'Full EU visibility with custom website',
            'monthly_price': 199.00,
            'yearly_price': 1990.00,
            'max_listings': 0,  # Unlimited
            'can_create_website': True,
            'can_choose_domain': True,
            'can_upload_logo': True,
            'featured_listings': True,
            'analytics_access': True,
            'priority_support': True,
            'api_access': True,
            'sort_order': 4
        }
    ]
    
    for plan_data in plans_data:
        plan, created = SubscriptionPlan.objects.get_or_create(
            plan_type=plan_data['plan_type'],
            defaults=plan_data
        )
        if created:
            print(f"Created plan: {plan.name}")
        else:
            print(f"Plan already exists: {plan.name}")
    
    print("Creating categories...")
    
    # Create main categories
    categories_data = [
        {'name': 'Restaurants', 'icon': '🍽️', 'description': 'Dining and food services'},
        {'name': 'Technology', 'icon': '💻', 'description': 'IT and technology services'},
        {'name': 'Healthcare', 'icon': '🏥', 'description': 'Medical and health services'},
        {'name': 'Education', 'icon': '🎓', 'description': 'Educational institutions and services'},
        {'name': 'Professional Services', 'icon': '💼', 'description': 'Business and professional services'},
        {'name': 'Retail', 'icon': '🛍️', 'description': 'Shopping and retail businesses'},
        {'name': 'Entertainment', 'icon': '🎭', 'description': 'Entertainment and leisure'},
        {'name': 'Automotive', 'icon': '🚗', 'description': 'Automotive services and sales'},
        {'name': 'Real Estate', 'icon': '🏠', 'description': 'Property and real estate services'},
        {'name': 'Beauty & Wellness', 'icon': '💆', 'description': 'Beauty and wellness services'},
    ]
    
    for cat_data in categories_data:
        slug = cat_data['name'].lower().replace(' ', '-').replace('&', 'and')
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'slug': slug,
                'icon': cat_data['icon'],
                'description': cat_data['description']
            }
        )
        if created:
            print(f"Created category: {category.name}")
    
    print("Creating EU countries...")
    
    # Create EU countries
    eu_countries = [
        {'name': 'Austria', 'code': 'AT'},
        {'name': 'Belgium', 'code': 'BE'},
        {'name': 'Bulgaria', 'code': 'BG'},
        {'name': 'Croatia', 'code': 'HR'},
        {'name': 'Cyprus', 'code': 'CY'},
        {'name': 'Czech Republic', 'code': 'CZ'},
        {'name': 'Denmark', 'code': 'DK'},
        {'name': 'Estonia', 'code': 'EE'},
        {'name': 'Finland', 'code': 'FI'},
        {'name': 'France', 'code': 'FR'},
        {'name': 'Germany', 'code': 'DE'},
        {'name': 'Greece', 'code': 'GR'},
        {'name': 'Hungary', 'code': 'HU'},
        {'name': 'Ireland', 'code': 'IE'},
        {'name': 'Italy', 'code': 'IT'},
        {'name': 'Latvia', 'code': 'LV'},
        {'name': 'Lithuania', 'code': 'LT'},
        {'name': 'Luxembourg', 'code': 'LU'},
        {'name': 'Malta', 'code': 'MT'},
        {'name': 'Netherlands', 'code': 'NL'},
        {'name': 'Poland', 'code': 'PL'},
        {'name': 'Portugal', 'code': 'PT'},
        {'name': 'Romania', 'code': 'RO'},
        {'name': 'Slovakia', 'code': 'SK'},
        {'name': 'Slovenia', 'code': 'SI'},
        {'name': 'Spain', 'code': 'ES'},
        {'name': 'Sweden', 'code': 'SE'},
    ]
    
    for country_data in eu_countries:
        country, created = Country.objects.get_or_create(
            code=country_data['code'],
            defaults={
                'name': country_data['name'],
                'is_eu_member': True
            }
        )
        if created:
            print(f"Created country: {country.name}")
    
    print("Creating admin user...")
    
    # Create admin user
    admin_email = "admin@listacross.eu"
    if not CustomUser.objects.filter(email=admin_email).exists():
        admin_user = CustomUser.objects.create_superuser(
            email=admin_email,
            password="admin123",
            first_name="Admin",
            last_name="User",
            subscription_type="eu"
        )
        print(f"Created admin user: {admin_email} (password: admin123)")
    else:
        print("Admin user already exists")
    
    print("Initial data creation completed!")

if __name__ == '__main__':
    create_initial_data()