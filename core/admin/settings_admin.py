from django.contrib import admin
from core.models import SiteSettings

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'site_description', 'contact_email', 'support_email', 'default_language')
        }),
        ('Feature Settings', {
            'fields': ('enable_registration', 'enable_comments', 'maintenance_mode'),
            'description': 'Control site features and functionality'
        }),
        ('Branding', {
            'fields': ('logo', 'favicon', 'footer_logo'),
            'classes': ('collapse',)
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'linkedin_url', 'instagram_url'),
            'classes': ('collapse',)
        }),
        ('SEO Defaults', {
            'fields': ('default_title', 'default_description', 'default_keywords', 'og_image_url'),
            'classes': ('collapse',)
        }),
        ('Analytics', {
            'fields': ('analytics_code',),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of settings
        return False
    
    def has_add_permission(self, request):
        # Only allow one settings instance
        return not SiteSettings.objects.exists()