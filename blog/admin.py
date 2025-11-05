from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from core.admin.seo_admin import SEOFirstAdmin
from .models import BlogCategory, BlogPost


@admin.register(BlogCategory)
class BlogCategoryAdmin(SEOFirstAdmin):
    list_display = ['name_en', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name_en', 'name_fr', 'name_nl', 'description_en']
    prepopulated_fields = {'slug': ('name_en',)}
    
    fieldsets = (
        SEOFirstAdmin.seo_fieldset,  # SEO at top with live preview
        (_('Category Names'), {
            'fields': ('name_en', 'name_fr', 'name_nl', 'name_pt', 'name_de', 'name_es', 'name_ar', 'slug')
        }),
        (_('Category Descriptions'), {
            'fields': ('description_en', 'description_fr', 'description_nl', 'description_pt', 'description_de', 'description_es', 'description_ar'),
            'classes': ('collapse',)
        }),
        (_('Settings'), {
            'fields': ('is_active',)
        }),
    )


@admin.register(BlogPost)
class BlogPostAdmin(SEOFirstAdmin):
    list_display = ['title_en', 'author', 'category', 'status', 'is_featured', 'published_at', 'created_at']
    list_filter = ['status', 'is_featured', 'category', 'author', 'published_at', 'created_at']
    search_fields = ['title_en', 'title_fr', 'title_nl', 'excerpt_en', 'content_en']
    prepopulated_fields = {'slug': ('title_en',)}
    date_hierarchy = 'published_at'
    
    fieldsets = (
        SEOFirstAdmin.seo_fieldset,  # SEO at top with live preview
        (_('Post Titles'), {
            'fields': ('title_en', 'title_fr', 'title_nl', 'title_pt', 'title_de', 'title_es', 'title_ar', 'slug')
        }),
        (_('Post Excerpts'), {
            'fields': ('excerpt_en', 'excerpt_fr', 'excerpt_nl', 'excerpt_pt', 'excerpt_de', 'excerpt_es', 'excerpt_ar'),
            'classes': ('collapse',)
        }),
        (_('Post Content'), {
            'fields': ('content_en', 'content_fr', 'content_nl', 'content_pt', 'content_de', 'content_es', 'content_ar'),
            'classes': ('collapse',)
        }),
        (_('Media & Publication'), {
            'fields': ('cover_image', 'author', 'category', 'status', 'is_featured', 'published_at'),
            'description': 'Control when and how this post appears on your site.'
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Auto-set published_at when status changes to published."""
        if obj.status == 'published' and not obj.published_at:
            obj.published_at = timezone.now()
        elif obj.status != 'published':
            obj.published_at = None
            
        if not change:  # New post
            obj.author = request.user
            
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category')