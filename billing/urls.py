from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('subscriptions/', views.subscription_list, name='subscription-list'),
    path('invoices/', views.invoice_list, name='invoice-list'),
]