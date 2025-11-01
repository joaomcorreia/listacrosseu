from django.db import models


class SeoFieldsMixin(models.Model):
    """SEO fields mixin for all content types that need SEO optimization"""
    meta_title = models.CharField(max_length=180, blank=True)
    meta_description = models.CharField(max_length=320, blank=True)
    canonical_url = models.URLField(blank=True)
    noindex = models.BooleanField(default=False)
    nofollow = models.BooleanField(default=False)
    og_image = models.URLField(blank=True, help_text="Absolute URL to social/OG image.")
    meta_json = models.JSONField(blank=True, null=True, help_text="Arbitrary JSON for extra meta / JSON-LD.")
    
    class Meta:
        abstract = True
    
    def seo_title(self):
        """Return SEO title or fallback to regular title"""
        title_attr = getattr(self, "title", "") or ""
        return self.meta_title or title_attr