from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator, MaxLengthValidator
from django.utils import timezone
from django.urls import reverse
import json


class Country(models.Model):
    """EU Countries for localized SEO pages"""
    code = models.CharField(
        max_length=2, 
        unique=True,
        validators=[RegexValidator(r'^[A-Z]{2}$', 'Country code must be 2 uppercase letters')]
    )
    name = models.CharField(max_length=100)
    default_locale = models.CharField(
        max_length=5, 
        default='en',
        help_text='Default language locale for this country (e.g., en, fr, nl)'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Countries'

    def __str__(self):
        return f"{self.name} ({self.code})"


class Language(models.Model):
    """Supported languages for multilingual SEO"""
    code = models.CharField(
        max_length=2, 
        unique=True,
        validators=[RegexValidator(r'^[a-z]{2}$', 'Language code must be 2 lowercase letters')]
    )
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class SeoPlan(models.Model):
    """SEO feature tiers - Basic/Growth/Premium"""
    PLAN_CHOICES = [
        ('basic', 'Basic'),
        ('growth', 'Growth'),
        ('premium', 'Premium'),
    ]
    
    name = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    slug = models.SlugField(unique=True)
    features = models.JSONField(
        default=dict,
        help_text='JSON object defining available features for this plan'
    )
    order = models.PositiveIntegerField(default=0, help_text='Display order (0=Basic, 1=Growth, 2=Premium)')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.get_name_display()

    def has_feature(self, feature_key):
        """Check if this plan includes a specific feature"""
        return self.features.get(feature_key, False)


class SeoPage(models.Model):
    """Core SEO page entity with plan-gated features"""
    
    PAGE_TYPE_CHOICES = [
        ('home', 'Home'),
        ('service', 'Service'),
        ('city', 'City'),
        ('country', 'Country'),
        ('blog', 'Blog'),
        ('custom', 'Custom'),
    ]
    
    ROBOTS_CHOICES = [
        ('index,follow', 'Index, Follow'),
        ('index,nofollow', 'Index, No Follow'),
        ('noindex,follow', 'No Index, Follow'),
        ('noindex,nofollow', 'No Index, No Follow'),
    ]

    # Core identifiers
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200)
    page_type = models.CharField(max_length=20, choices=PAGE_TYPE_CHOICES, default='custom')
    plan = models.ForeignKey(SeoPlan, on_delete=models.CASCADE, default=1)  # Basic plan by default
    
    # Basic tier SEO fields (always available)
    meta_title = models.CharField(
        max_length=60, 
        validators=[MaxLengthValidator(60)],
        help_text='Page title (max 60 chars for optimal SEO)'
    )
    meta_description = models.TextField(
        max_length=160, 
        validators=[MaxLengthValidator(160)],
        help_text='Meta description (max 160 chars)'
    )
    h1 = models.CharField(max_length=100, help_text='Main page heading')
    h2 = models.CharField(max_length=100, blank=True, help_text='Secondary heading')
    canonical_url = models.URLField(blank=True, help_text='Canonical URL for this page')
    robots = models.CharField(max_length=20, choices=ROBOTS_CHOICES, default='index,follow')
    image_alt_fallback = models.CharField(max_length=125, blank=True, help_text='Default alt text for images')
    
    # Growth tier fields (requires Growth or Premium plan)
    keywords_hint = models.TextField(
        blank=True, 
        help_text='Comma-separated keywords for content optimization'
    )
    internal_links = models.JSONField(
        default=list, 
        blank=True,
        help_text='Array of {title, href} objects for internal linking'
    )
    sitemap_include = models.BooleanField(default=True, help_text='Include in XML sitemap')
    og_title = models.CharField(max_length=60, blank=True, help_text='Open Graph title')
    og_description = models.TextField(max_length=160, blank=True, help_text='Open Graph description')
    og_image_url = models.URLField(blank=True, help_text='Open Graph image URL')
    twitter_card = models.CharField(
        max_length=20, 
        choices=[
            ('summary', 'Summary'),
            ('summary_large_image', 'Summary Large Image'),
            ('app', 'App'),
            ('player', 'Player')
        ],
        default='summary',
        blank=True
    )
    twitter_image_url = models.URLField(blank=True, help_text='Twitter card image URL')
    
    # Premium tier fields (requires Premium plan)
    json_ld = models.TextField(
        blank=True,
        help_text='JSON-LD structured data (Premium feature)'
    )
    breadcrumbs = models.JSONField(
        default=list,
        blank=True,
        help_text='Breadcrumb navigation structure'
    )
    local_business_schema = models.JSONField(
        default=dict,
        blank=True,
        help_text='Local business schema markup'
    )
    service_schema = models.JSONField(
        default=dict,
        blank=True,
        help_text='Service schema markup'
    )
    
    # Publishing and metadata
    is_published = models.BooleanField(default=False)
    publish_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['country', 'language', 'slug', 'page_type']
        ordering = ['-updated_at']

    def __str__(self):
        country_code = self.country.code if self.country else 'GLOBAL'
        return f"{self.meta_title} ({country_code}-{self.language.code})"

    def get_absolute_url(self):
        """Generate the frontend URL for this page"""
        if not self.country:
            return f"/{self.language.code}/"
        
        # Build hierarchical URL based on page type
        if self.page_type == 'home':
            return f"/{self.language.code}/"
        elif self.page_type == 'country':
            return f"/{self.language.code}/{self.country.code.lower()}/"
        elif self.page_type == 'city':
            return f"/{self.language.code}/{self.country.code.lower()}/{self.slug}/"
        elif self.page_type == 'service':
            # Assumes city is in slug path or derived from other pages
            return f"/{self.language.code}/{self.country.code.lower()}/porto/{self.slug}/"
        else:
            return f"/{self.language.code}/{self.slug}/"

    def can_use_feature(self, feature_name):
        """Check if current plan allows use of a specific feature"""
        feature_map = {
            # Basic features (always available)
            'meta_title': True,
            'meta_description': True,
            'h1': True,
            'h2': True,
            'canonical_url': True,
            'robots': True,
            'image_alt_fallback': True,
            
            # Growth features
            'keywords_hint': self.plan.order >= 1,
            'internal_links': self.plan.order >= 1,
            'sitemap_include': self.plan.order >= 1,
            'og_title': self.plan.order >= 1,
            'og_description': self.plan.order >= 1,
            'og_image_url': self.plan.order >= 1,
            'twitter_card': self.plan.order >= 1,
            'twitter_image_url': self.plan.order >= 1,
            
            # Premium features
            'json_ld': self.plan.order >= 2,
            'breadcrumbs': self.plan.order >= 2,
            'local_business_schema': self.plan.order >= 2,
            'service_schema': self.plan.order >= 2,
        }
        return feature_map.get(feature_name, False)

    def save(self, *args, **kwargs):
        # Auto-generate canonical URL if not provided
        if not self.canonical_url:
            self.canonical_url = f"https://listacross.eu{self.get_absolute_url()}"
        
        # Set publish_at if being published for the first time
        if self.is_published and not self.publish_at:
            self.publish_at = timezone.now()
            
        super().save(*args, **kwargs)


class SeoContentBlock(models.Model):
    """Additional content blocks for SEO pages"""
    seo_page = models.ForeignKey(SeoPage, on_delete=models.CASCADE, related_name='content_blocks')
    key = models.CharField(max_length=50, help_text='Content block identifier (e.g., intro, features, cta)')
    content = models.TextField(help_text='Rich text or markdown content')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['seo_page', 'key']
        ordering = ['order']

    def __str__(self):
        return f"{self.seo_page.meta_title} - {self.key}"
