from django.db import models
from django.core.exceptions import ValidationError


class SiteSetting(models.Model):
    """Site-wide settings including logos and basic information"""
    
    # Basic site information
    site_name = models.CharField(max_length=200, default='ListAcrossEU')
    site_tagline = models.CharField(max_length=500, default='European Business Directory')
    contact_email = models.EmailField(default='contact@listacrosseu.com')
    support_email = models.EmailField(default='support@listacrosseu.com')
    phone = models.CharField(max_length=50, default='+1 (555) 123-4567')
    address = models.TextField(default='Brussels, Belgium')
    
    # Logo and branding
    logo = models.ImageField(upload_to='site/logos/', null=True, blank=True, 
                            help_text='Site logo - PNG or SVG recommended, max 2MB, 200x200px')
    favicon = models.ImageField(upload_to='site/favicons/', null=True, blank=True,
                               help_text='Site favicon - ICO or PNG, 16x16 or 32x32px')
    
    # Navigation settings
    NAVIGATION_CHOICES = [
        ('flags', 'Flags Only'),
        ('names', 'Names Only'),
        ('both', 'Flags and Names'),
    ]
    navigation_display_mode = models.CharField(
        max_length=10, 
        choices=NAVIGATION_CHOICES, 
        default='both',
        help_text='How to display language selector in navigation'
    )
    
    # Animation settings
    enable_nav_animation = models.BooleanField(
        default=True,
        help_text='Enable animated border under navigation'
    )
    nav_animation_colors = models.CharField(
        max_length=200,
        default='from-blue-500 via-purple-500 to-indigo-500',
        help_text='Tailwind gradient colors for navigation border animation'
    )
    
    ANIMATION_SPEED_CHOICES = [
        ('slow', 'Slow'),
        ('medium', 'Medium'), 
        ('fast', 'Fast'),
    ]
    nav_animation_speed = models.CharField(
        max_length=10,
        choices=ANIMATION_SPEED_CHOICES,
        default='medium',
        help_text='Speed of navigation border animation'
    )
    
    # Slideshow animation settings (for future use)
    enable_slideshow_animation = models.BooleanField(
        default=True,
        help_text='Enable slideshow animations on homepage'
    )
    slideshow_animation_speed = models.CharField(
        max_length=10,
        choices=ANIMATION_SPEED_CHOICES,
        default='medium',
        help_text='Speed of slideshow animations'
    )
    
    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Site Setting'
        verbose_name_plural = 'Site Settings'
    
    def __str__(self):
        return f"Site Settings - {self.site_name}"
    
    def clean(self):
        """Validate file uploads"""
        if self.logo and self.logo.size > 2 * 1024 * 1024:  # 2MB
            raise ValidationError({'logo': 'Logo file size must be under 2MB.'})
        
        if self.favicon and self.favicon.size > 1 * 1024 * 1024:  # 1MB
            raise ValidationError({'favicon': 'Favicon file size must be under 1MB.'})
    
    def save(self, *args, **kwargs):
        # Ensure only one settings instance exists (singleton pattern)
        if not self.pk and SiteSetting.objects.exists():
            raise ValidationError('Only one SiteSetting instance is allowed.')
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get or create the site settings instance"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings
