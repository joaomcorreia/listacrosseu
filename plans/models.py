from django.db import models

PLAN_KEYS = (("free", "Free"), ("product", "Product Page"), ("premium", "Premium"))


class Plan(models.Model):
    key = models.CharField(max_length=32, unique=True, choices=PLAN_KEYS)
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    entitlements = models.JSONField(default=dict)
    highlights = models.JSONField(default=list)
    priority_weight = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class VisibilityProfile(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    include_in_sitemap = models.BooleanField(default=True)
    force_noindex = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    featured_weight = models.IntegerField(default=0)
    badges = models.JSONField(default=list)
    
    def __str__(self):
        return f"{self.plan.name} / featured={self.featured} / w={self.featured_weight}"
