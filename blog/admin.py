from django.contrib import admin
from assist.admin_mixins import AIMixin
from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "color"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name", "description"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin, AIMixin):
    list_display = ["title", "language", "author", "category", "plan_key", "is_published", "is_featured", "published_at"]
    list_filter = ["language", "is_published", "is_featured", "category", "author", "visibility__plan", "created_at"]
    search_fields = ["title", "excerpt", "content"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["related_posts"]
    date_hierarchy = "published_at"
    actions = ["ai_suggest"]
    
    fieldsets = [
        ("Content", {
            "fields": ["title", "slug", "language", "author", "category", "excerpt", "content", "featured_image"]
        }),
        ("Publishing", {
            "fields": ["is_published", "is_featured", "published_at"]
        }),
        ("Visibility", {
            "fields": ["visibility"]
        }),
        ("Relationships", {
            "fields": ["related_posts"],
            "classes": ["collapse"]
        }),
        ("SEO & Social", {
            "fields": ["meta_title", "meta_description", "canonical_url", "noindex", "nofollow", "og_image", "meta_json"],
            "classes": ["collapse"]
        }),
    ]
    
    def plan_key(self, obj):
        return getattr(getattr(obj.visibility, "plan", None), "key", "-")
    plan_key.short_description = "Plan"
    
    def save_model(self, request, obj, form, change):
        if not change:  # New post
            obj.author = request.user
        super().save_model(request, obj, form, change)
