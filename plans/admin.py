from django.contrib import admin
from .models import Plan, VisibilityProfile


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "key", "priority_weight", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "key", "description")
    fieldsets = (
        ("Basics", {"fields": ("key", "name", "description", "is_active")}),
        ("Entitlements", {"fields": ("entitlements", "highlights", "priority_weight")}),
    )


@admin.register(VisibilityProfile)
class VisibilityProfileAdmin(admin.ModelAdmin):
    list_display = ("plan", "featured", "featured_weight", "include_in_sitemap", "force_noindex")
    list_filter = ("plan", "featured", "include_in_sitemap", "force_noindex")
