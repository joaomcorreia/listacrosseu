from django.contrib import admin
from django.utils.html import format_html
from .models import SiteSetting


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    """Admin interface for Site Settings"""
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'site_tagline')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'support_email', 'phone', 'address')
        }),
        ('Branding', {
            'fields': ('logo', 'logo_preview', 'favicon', 'favicon_preview'),
            'description': 'Upload your site logo and favicon here.'
        }),
    )
    
    readonly_fields = ('logo_preview', 'favicon_preview')
    
    def logo_preview(self, obj):
        """Display logo preview in admin"""
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px;" />',
                obj.logo.url
            )
        return "No logo uploaded"
    logo_preview.short_description = "Logo Preview"
    
    def favicon_preview(self, obj):
        """Display favicon preview in admin"""
        if obj.favicon:
            return format_html(
                '<img src="{}" style="max-width: 32px; max-height: 32px;" />',
                obj.favicon.url
            )
        return "No favicon uploaded"
    favicon_preview.short_description = "Favicon Preview"
    
    def has_add_permission(self, request):
        """Only allow one instance"""
        return not SiteSetting.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of settings"""
        return False
