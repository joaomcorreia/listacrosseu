from django.db import models
from django.utils.translation import gettext_lazy as _


class SEOSettings(models.Model):
    """Global SEO settings"""
    site_name = models.CharField(max_length=100, default='ListAcross EU', verbose_name=_('Site Name'))
    site_description = models.TextField(verbose_name=_('Site Description'))
    default_meta_title = models.CharField(max_length=200, verbose_name=_('Default Meta Title'))
    default_meta_description = models.CharField(max_length=300, verbose_name=_('Default Meta Description'))
    
    # Social Media
    facebook_url = models.URLField(blank=True, verbose_name=_('Facebook URL'))
    twitter_url = models.URLField(blank=True, verbose_name=_('Twitter URL'))
    linkedin_url = models.URLField(blank=True, verbose_name=_('LinkedIn URL'))
    
    # Analytics
    google_analytics_id = models.CharField(max_length=20, blank=True, verbose_name=_('Google Analytics ID'))
    google_tag_manager_id = models.CharField(max_length=20, blank=True, verbose_name=_('Google Tag Manager ID'))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('SEO Settings')
        verbose_name_plural = _('SEO Settings')
    
    def __str__(self):
        return self.site_name