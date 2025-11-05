from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_published', 'created_at', 'updated_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('title', 'slug', 'content', 'is_published')
        }),
        (_('Translations'), {
            'fields': ('content_en', 'content_fr', 'content_nl', 'content_pt', 'content_de', 'content_es', 'content_ar'),
            'classes': ('collapse',)
        }),
    )