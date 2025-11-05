from django.contrib import admin
from assist.admin_mixins import AIMixin
from .models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin, AIMixin):
    list_display = ("title", "slug", "language", "plan_key", "is_published", "updated_at")
    list_filter = ("language", "is_published", "visibility__plan")
    search_fields = ("title", "slug", "meta_title", "meta_description", "body")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    actions = ["ai_suggest"]
    fieldsets = (
        ("Route & Status", {"fields": ("slug", "language", "is_published", "template_key")}),
        ("Content", {"fields": ("title", "body")}),
        ("Visibility", {"fields": ("visibility",)}),
        ("SEO", {"fields": ("meta_title", "meta_description", "canonical_url", ("noindex", "nofollow"), "og_image", "meta_json")}),
        ("System", {"fields": ("created_at", "updated_at")}),
    )
    
    def plan_key(self, obj):
        return getattr(getattr(obj.visibility, "plan", None), "key", "-")
    plan_key.short_description = "Plan"
