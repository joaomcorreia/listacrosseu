from django.db import models
from django.core.cache import cache

class SiteSettings(models.Model):
    """
    Site-wide settings model. Uses singleton pattern - only one instance should exist.
    """
    site_name = models.CharField(max_length=100, default='ListAcross EU')
    site_description = models.TextField(default='The premier business directory for European markets')
    contact_email = models.EmailField(default='contact@listacrosseu.com')
    support_email = models.EmailField(default='support@listacrosseu.com')
    default_language = models.CharField(max_length=5, default='eu')
    
    # Feature toggles
    enable_registration = models.BooleanField(default=True)
    enable_comments = models.BooleanField(default=True)
    maintenance_mode = models.BooleanField(default=False, help_text='When enabled, site shows maintenance page to non-admin users')
    enable_star_animation = models.BooleanField(default=True, help_text='Enable animated EU stars on hero section')
    
    # Analytics
    analytics_code = models.TextField(blank=True, help_text='Google Analytics or other tracking code')
    
    # Branding
    logo = models.URLField(blank=True)
    favicon = models.URLField(blank=True)
    footer_logo = models.URLField(blank=True)
    
    # Social links
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True) 
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    
    # SEO defaults
    default_title = models.CharField(max_length=200, blank=True)
    default_description = models.TextField(blank=True)
    default_keywords = models.TextField(blank=True)
    og_image_url = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'
    
    def __str__(self):
        return f'Site Settings ({self.site_name})'
    
    def save(self, *args, **kwargs):
        # Singleton pattern - only allow one instance
        if not self.pk and SiteSettings.objects.exists():
            # If this is a new instance and one already exists, update the existing one
            existing = SiteSettings.objects.first()
            existing.__dict__.update(self.__dict__)
            existing.save()
            return existing
        
        # Clear cache when settings are updated
        cache.delete('site_settings')
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get site settings with caching"""
        settings = cache.get('site_settings')
        if settings is None:
            settings, created = cls.objects.get_or_create(pk=1)
            cache.set('site_settings', settings, 60 * 60)  # Cache for 1 hour
        return settings
    
    @classmethod
    def is_maintenance_mode(cls):
        """Quick check for maintenance mode"""
        return cls.get_settings().maintenance_mode