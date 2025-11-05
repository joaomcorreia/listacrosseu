from django.db import models
from django.utils.translation import gettext_lazy as _


class Page(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    slug = models.SlugField(unique=True, verbose_name=_('Slug'))
    content = models.TextField(verbose_name=_('Content'))
    
    # Multi-language content
    content_en = models.TextField(verbose_name=_('Content (English)'), blank=True)
    content_fr = models.TextField(verbose_name=_('Content (French)'), blank=True)
    content_nl = models.TextField(verbose_name=_('Content (Dutch)'), blank=True)
    content_pt = models.TextField(verbose_name=_('Content (Portuguese)'), blank=True)
    content_de = models.TextField(verbose_name=_('Content (German)'), blank=True)
    content_es = models.TextField(verbose_name=_('Content (Spanish)'), blank=True)
    content_ar = models.TextField(verbose_name=_('Content (Arabic)'), blank=True)
    
    is_published = models.BooleanField(default=True, verbose_name=_('Is Published'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
        ordering = ['title']
    
    def __str__(self):
        return self.title
    
    def get_content_for_language(self, language_code):
        """Get page content in specific language"""
        if language_code == 'en' and self.content_en:
            return self.content_en
        elif language_code == 'fr' and self.content_fr:
            return self.content_fr
        elif language_code == 'nl' and self.content_nl:
            return self.content_nl
        elif language_code == 'pt' and self.content_pt:
            return self.content_pt
        elif language_code == 'de' and self.content_de:
            return self.content_de
        elif language_code == 'es' and self.content_es:
            return self.content_es
        elif language_code == 'ar' and self.content_ar:
            return self.content_ar
        return self.content