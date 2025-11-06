from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from core.models.seo import SEOMixin
import uuid


class BlogCategory(SEOMixin, models.Model):
    # Multilingual name fields
    name_en = models.CharField(max_length=100, default='', verbose_name=_('Category Name (English)'))
    name_fr = models.CharField(max_length=100, blank=True, default='', verbose_name=_('Category Name (French)'))
    name_nl = models.CharField(max_length=100, blank=True, default='', verbose_name=_('Category Name (Dutch)'))
    name_pt = models.CharField(max_length=100, blank=True, default='', verbose_name=_('Category Name (Portuguese)'))
    name_de = models.CharField(max_length=100, blank=True, default='', verbose_name=_('Category Name (German)'))
    name_es = models.CharField(max_length=100, blank=True, default='', verbose_name=_('Category Name (Spanish)'))
    name_ar = models.CharField(max_length=100, blank=True, default='', verbose_name=_('Category Name (Arabic)'))
    
    slug = models.SlugField(unique=True)
    
    # Multilingual description fields
    description_en = models.TextField(blank=True, default='', verbose_name=_('Description (English)'))
    description_fr = models.TextField(blank=True, default='', verbose_name=_('Description (French)'))
    description_nl = models.TextField(blank=True, default='', verbose_name=_('Description (Dutch)'))
    description_pt = models.TextField(blank=True, default='', verbose_name=_('Description (Portuguese)'))
    description_de = models.TextField(blank=True, default='', verbose_name=_('Description (German)'))
    description_es = models.TextField(blank=True, default='', verbose_name=_('Description (Spanish)'))
    description_ar = models.TextField(blank=True, default='', verbose_name=_('Description (Arabic)'))
    
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Legacy fields for backward compatibility
    @property
    def name(self):
        return self.name_en
    
    @property 
    def description(self):
        return self.description_en
    
    def get_name(self, lang='en'):
        """Get category name in specified language, fallback to English"""
        field_name = f'name_{lang}'
        if hasattr(self, field_name):
            value = getattr(self, field_name)
            return value if value else self.name_en
        return self.name_en
    
    def get_description(self, lang='en'):
        """Get category description in specified language, fallback to English"""
        field_name = f'description_{lang}'
        if hasattr(self, field_name):
            value = getattr(self, field_name)
            return value if value else self.description_en
        return self.description_en
    
    class Meta:
        verbose_name = _('Blog Category')
        verbose_name_plural = _('Blog Categories')
        ordering = ['name_en']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})


class BlogPost(SEOMixin, models.Model):
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('review', _('Under Review')),
        ('published', _('Published')),
        ('archived', _('Archived')),
    ]
    
    # Multilingual title fields
    title_en = models.CharField(max_length=200, default='', verbose_name=_('Title (English)'))
    title_fr = models.CharField(max_length=200, blank=True, default='', verbose_name=_('Title (French)'))
    title_nl = models.CharField(max_length=200, blank=True, default='', verbose_name=_('Title (Dutch)'))
    title_pt = models.CharField(max_length=200, blank=True, default='', verbose_name=_('Title (Portuguese)'))
    title_de = models.CharField(max_length=200, blank=True, default='', verbose_name=_('Title (German)'))
    title_es = models.CharField(max_length=200, blank=True, default='', verbose_name=_('Title (Spanish)'))
    title_ar = models.CharField(max_length=200, blank=True, default='', verbose_name=_('Title (Arabic)'))
    
    slug = models.SlugField(unique=True)
    
    # Multilingual excerpt fields
    excerpt_en = models.TextField(max_length=300, blank=True, default='', verbose_name=_('Excerpt (English)'))
    excerpt_fr = models.TextField(max_length=300, blank=True, default='', verbose_name=_('Excerpt (French)'))
    excerpt_nl = models.TextField(max_length=300, blank=True, default='', verbose_name=_('Excerpt (Dutch)'))
    excerpt_pt = models.TextField(max_length=300, blank=True, default='', verbose_name=_('Excerpt (Portuguese)'))
    excerpt_de = models.TextField(max_length=300, blank=True, default='', verbose_name=_('Excerpt (German)'))
    excerpt_es = models.TextField(max_length=300, blank=True, default='', verbose_name=_('Excerpt (Spanish)'))
    excerpt_ar = models.TextField(max_length=300, blank=True, default='', verbose_name=_('Excerpt (Arabic)'))
    
    # Multilingual content fields
    content_en = models.TextField(default='', verbose_name=_('Content (English)'))
    content_fr = models.TextField(blank=True, default='', verbose_name=_('Content (French)'))
    content_nl = models.TextField(blank=True, default='', verbose_name=_('Content (Dutch)'))
    content_pt = models.TextField(blank=True, default='', verbose_name=_('Content (Portuguese)'))
    content_de = models.TextField(blank=True, default='', verbose_name=_('Content (German)'))
    content_es = models.TextField(blank=True, default='', verbose_name=_('Content (Spanish)'))
    content_ar = models.TextField(blank=True, default='', verbose_name=_('Content (Arabic)'))
    
    # Legacy properties for backward compatibility
    @property
    def title(self):
        return self.title_en
    
    @property
    def excerpt(self):
        return self.excerpt_en
    
    @property
    def content(self):
        return self.content_en
    
    def get_title(self, lang='en'):
        """Get blog post title in specified language, fallback to English"""
        field_name = f'title_{lang}'
        if hasattr(self, field_name):
            value = getattr(self, field_name)
            return value if value else self.title_en
        return self.title_en
    
    def get_excerpt(self, lang='en'):
        """Get blog post excerpt in specified language, fallback to English"""
        field_name = f'excerpt_{lang}'
        if hasattr(self, field_name):
            value = getattr(self, field_name)
            return value if value else self.excerpt_en
        return self.excerpt_en
    
    def get_content(self, lang='en'):
        """Get blog post content in specified language, fallback to English"""
        field_name = f'content_{lang}'
        if hasattr(self, field_name):
            value = getattr(self, field_name)
            return value if value else self.content_en
        return self.content_en
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Author'))
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Category'))
    
    cover_image = models.URLField(blank=True, verbose_name=_('Cover Image'))
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name=_('Status'))
    is_featured = models.BooleanField(default=False, verbose_name=_('Is Featured'))
    
    published_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Published At'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Blog Post')
        verbose_name_plural = _('Blog Posts')
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'slug': self.slug})
    
    @property
    def is_published(self):
        return self.status == 'published' and self.published_at


class AIGeneration(models.Model):
    """Track AI content generation activities"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stage = models.CharField(max_length=20, choices=[
        ('outline', 'Outline Generation'),
        ('draft', 'Draft Generation'),
        ('seo', 'SEO Generation'),
        ('translate', 'Translation')
    ])
    language = models.CharField(max_length=10, default='en')
    input_payload = models.JSONField()
    output_payload = models.JSONField()
    sources = models.JSONField(default=list, blank=True)  # List of source URLs
    quality_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'AI Generation Log'
        verbose_name_plural = 'AI Generation Logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.stage} - {self.language} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"