from django.contrib import admin
from .models import SubscriptionPlan, Subscription, SubscriptionUsage, Invoice


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'plan_type', 'monthly_price', 'yearly_price',
        'max_listings', 'can_create_website', 'is_active', 'sort_order'
    ]
    list_filter = ['plan_type', 'is_active', 'can_create_website']
    search_fields = ['name', 'description']
    ordering = ['sort_order']
    
    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'plan_type', 'description']
        }),
        ('Pricing', {
            'fields': ['monthly_price', 'yearly_price']
        }),
        ('Features', {
            'fields': [
                'max_listings', 'can_create_website', 'can_choose_domain',
                'can_upload_logo', 'priority_support', 'featured_listings',
                'analytics_access', 'api_access'
            ]
        }),
        ('Stripe Integration', {
            'fields': ['stripe_monthly_price_id', 'stripe_yearly_price_id'],
            'classes': ['collapse']
        }),
        ('Settings', {
            'fields': ['is_active', 'sort_order']
        })
    ]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'plan', 'status', 'billing_period',
        'current_period_start', 'current_period_end', 'created_at'
    ]
    list_filter = ['status', 'billing_period', 'plan__plan_type', 'created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['id', 'stripe_subscription_id', 'stripe_customer_id', 'created_at']
    
    fieldsets = [
        ('Subscription Details', {
            'fields': ['user', 'plan', 'billing_period', 'status']
        }),
        ('Dates', {
            'fields': [
                'start_date', 'end_date', 'current_period_start',
                'current_period_end', 'trial_end', 'cancelled_at'
            ]
        }),
        ('Stripe Integration', {
            'fields': ['stripe_subscription_id', 'stripe_customer_id'],
            'classes': ['collapse']
        }),
        ('Metadata', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'plan')


@admin.register(SubscriptionUsage)
class SubscriptionUsageAdmin(admin.ModelAdmin):
    list_display = [
        'subscription', 'period_start', 'listings_used',
        'api_calls_used', 'storage_used', 'listings_remaining'
    ]
    list_filter = ['period_start', 'period_end']
    search_fields = ['subscription__user__email']
    readonly_fields = ['listings_remaining']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('subscription__user', 'subscription__plan')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        'invoice_number', 'subscription', 'status',
        'total_amount', 'issue_date', 'due_date', 'is_paid'
    ]
    list_filter = ['status', 'issue_date', 'due_date']
    search_fields = ['invoice_number', 'subscription__user__email']
    readonly_fields = ['id', 'is_paid', 'is_overdue', 'stripe_invoice_id']
    
    fieldsets = [
        ('Invoice Details', {
            'fields': ['subscription', 'invoice_number', 'status']
        }),
        ('Amounts', {
            'fields': ['subtotal', 'tax_amount', 'total_amount']
        }),
        ('Dates', {
            'fields': ['issue_date', 'due_date', 'paid_date']
        }),
        ('Stripe Integration', {
            'fields': ['stripe_invoice_id'],
            'classes': ['collapse']
        }),
        ('Files', {
            'fields': ['pdf_file'],
            'classes': ['collapse']
        }),
        ('Status', {
            'fields': ['is_paid', 'is_overdue'],
            'classes': ['collapse']
        })
    ]