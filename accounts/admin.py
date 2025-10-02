from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Custom admin interface for CustomUser model"""
    
    list_display = (
        'email', 'first_name', 'last_name', 'company_name',
        'subscription_type', 'subscription_active', 'is_verified',
        'created_at'
    )
    list_filter = (
        'subscription_type', 'subscription_active', 'is_verified',
        'marketing_emails', 'newsletter', 'created_at'
    )
    search_fields = ('email', 'first_name', 'last_name', 'company_name')
    ordering = ('-created_at',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Personal Info', {
            'fields': ('phone', 'company_name', 'profile_picture', 'bio', 'website')
        }),
        ('Address', {
            'fields': ('address', 'city', 'country', 'postal_code')
        }),
        ('Subscription', {
            'fields': ('subscription_type', 'subscription_active', 'subscription_expires')
        }),
        ('Verification', {
            'fields': ('is_verified', 'verification_documents')
        }),
        ('Marketing', {
            'fields': ('marketing_emails', 'newsletter')
        }),
        ('Metadata', {
            'fields': ('last_login_ip', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('email',)
        return self.readonly_fields