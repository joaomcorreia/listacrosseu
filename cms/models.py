from django.db import models
from common.seo import SeoFieldsMixin
from plans.models import VisibilityProfile

LANG_CHOICES = [
    ("en", "English"),
    ("nl", "Dutch"),
    ("fr", "French"),
    ("es", "Spanish"),
    ("pt", "Portuguese"),
    ("de", "German"),
    ("it", "Italian")
]


class Page(SeoFieldsMixin):
    """CMS Pages with full SEO control and multi-language support"""
    slug = models.SlugField(max_length=160)
    language = models.CharField(max_length=5, choices=LANG_CHOICES, default="en")
    is_published = models.BooleanField(default=True)
    template_key = models.CharField(max_length=80, blank=True, help_text="Optional template identifier.")
    title = models.CharField(max_length=160)
    body = models.TextField(blank=True, help_text="HTML or Markdown content.")
    visibility = models.ForeignKey(VisibilityProfile, on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ("slug", "language")
        indexes = [models.Index(fields=["slug", "language", "is_published"])]
    
    def __str__(self):
        return f"{self.title} [{self.language}]"
    
    def is_indexable(self):
        if self.visibility and self.visibility.force_noindex:
            return False
        return not self.noindex
    
    def effective_jsonld_allowed(self):
        plan = self.visibility.plan if self.visibility else None
        return bool(plan and plan.entitlements.get("jsonld", False))
