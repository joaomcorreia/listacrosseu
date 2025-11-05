from django.contrib import admin
from .models import SubscriptionPlan, UserSubscription, Invoice


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'currency', 'billing_period', 'is_active', 'created_at']
    list_filter = ['billing_period', 'is_active', 'created_at']
    search_fields = ['name', 'description']


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'start_date', 'end_date', 'is_active', 'auto_renew']
    list_filter = ['plan', 'is_active', 'auto_renew', 'start_date']
    search_fields = ['user__username', 'user__email', 'plan__name']
    date_hierarchy = 'start_date'


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'user', 'amount', 'currency', 'status', 'due_date', 'paid_at']
    list_filter = ['status', 'currency', 'created_at']
    search_fields = ['invoice_number', 'user__username', 'user__email']
    date_hierarchy = 'created_at'
    readonly_fields = ['invoice_number']