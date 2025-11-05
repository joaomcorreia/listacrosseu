from billing.models import SubscriptionPlan, UserSubscription, Invoice
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from decimal import Decimal
import uuid

# Create sample subscription plans
basic_plan, created = SubscriptionPlan.objects.get_or_create(
    name='Basic Plan',
    defaults={
        'description': 'Basic business listing with limited features',
        'price': Decimal('9.99'),
        'currency': 'EUR',
        'billing_period': 'monthly'
    }
)

premium_plan, created = SubscriptionPlan.objects.get_or_create(
    name='Premium Plan', 
    defaults={
        'description': 'Full-featured business listing with SEO tools',
        'price': Decimal('29.99'),
        'currency': 'EUR', 
        'billing_period': 'monthly'
    }
)

enterprise_plan, created = SubscriptionPlan.objects.get_or_create(
    name='Enterprise Plan',
    defaults={
        'description': 'Enterprise solution with multiple listings and analytics',
        'price': Decimal('299.99'),
        'currency': 'EUR',
        'billing_period': 'yearly'
    }
)

print(f'Created {SubscriptionPlan.objects.count()} subscription plans')
print('Sample billing data created successfully!')