from django.db import models
from django.core.validators import RegexValidator
import json

LANG_CODE_RE = RegexValidator(regex=r"^[a-z]{2}$", message="Use 2-letter lang codes, e.g., en, nl, fr, es, pt.")

class AssistantConfig(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("live", "Live"),
        ("archived", "Archived"),
    ]

    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="draft")
    default_lang = models.CharField(max_length=2, validators=[LANG_CODE_RE], default="en")
    supported_langs = models.JSONField(default=list, blank=True)  # Changed from ArrayField to JSONField for SQLite compatibility
    system_prompt = models.TextField(blank=True, default="")
    guardrails = models.JSONField(default=dict, blank=True)
    cta_text = models.JSONField(default=dict, blank=True)  # e.g. {"en":{"create_listing":"Advertise free", ...}, "nl":{...}}

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Assistant Configuration"
        verbose_name_plural = "Assistant Configurations"

    def __str__(self):
        return f"AssistantConfig #{self.id} ({self.status})"


class AssistantVersion(models.Model):
    config = models.ForeignKey("AssistantConfig", on_delete=models.CASCADE, related_name="versions")
    version = models.PositiveIntegerField()  # monotonic per config
    label = models.CharField(max_length=120, blank=True, default="")
    payload = models.JSONField()  # snapshot: prompt, langs, guardrails, cta_text
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("config", "version"),)
        ordering = ("-version",)

    def __str__(self):
        return f"v{self.version} ({self.created_at.isoformat()})"


class KnowledgeDoc(models.Model):
    TYPE_CHOICES = [
        ("kb_json", "KB JSON"),
        ("blog_md", "Blog Markdown"),
        ("pricing_json", "Pricing JSON"),
        ("faq_md", "FAQ Markdown"),
        ("external_url", "External URL"),
    ]
    slug = models.SlugField(max_length=120, unique=True)
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="kb_json")
    lang = models.CharField(max_length=5, default="en")  # en, nl, fr, es, pt, or 'multi'
    enabled = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)

    # Source: one of content (inline), source_path, or url
    content = models.TextField(blank=True, default="")
    source_path = models.CharField(max_length=300, blank=True, default="")
    url = models.URLField(blank=True, default="")

    # Ops
    checksum = models.CharField(max_length=64, blank=True, default="")
    embedded_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-enabled", "-priority", "slug")

    def __str__(self):
        return f"{self.slug} [{self.lang}]"


class Intent(models.Model):
    ANSWER_STYLE = [("short","Short"),("detailed","Detailed")]
    CTA_CHOICES = [
        ("create_listing","Create Listing"),
        ("upgrade_plan","Upgrade Plan"),
        ("start_jcw_build","Start JCW Build"),
        ("start_print_order","Start Print Order"),
        ("none","None"),
    ]

    name = models.SlugField(max_length=80, unique=True)  # e.g. pricing, website_build
    title = models.CharField(max_length=160)            # human label
    enabled = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)           # higher shows first
    examples = models.JSONField(default=list, blank=True)         # ["how much...", "pricing?"]
    keywords = models.JSONField(default=list, blank=True)         # ["price","cost","plan"]
    answer_style = models.CharField(max_length=12, choices=ANSWER_STYLE, default="short")
    primary_cta = models.CharField(max_length=40, choices=CTA_CHOICES, default="none")
    fallback_doc_slugs = models.JSONField(default=list, blank=True)  # ["plans_001","value_prop_001"]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-enabled","-priority","name")

    def __str__(self):
        return f"{self.name} ({'on' if self.enabled else 'off'})"