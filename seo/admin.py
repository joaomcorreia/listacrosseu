from django.contrib import admin
from .models import SEOSettings


@admin.register(SEOSettings)
class SEOSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'updated_at']
    
    def has_add_permission(self, request):
        # Allow only one instance of SEO settings
        return not SEOSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of SEO settings
        return False