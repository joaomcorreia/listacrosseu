from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Country, Language, SeoPlan, SeoPage, SeoContentBlock


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'default_locale', 'is_active', 'created_at']
    list_filter = ['is_active', 'default_locale']
    search_fields = ['code', 'name']
    readonly_fields = ['created_at']
    ordering = ['name']


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['code', 'name']
    readonly_fields = ['created_at']
    ordering = ['name']


@admin.register(SeoPlan)
class SeoPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active', 'feature_count']
    list_filter = ['is_active', 'name']
    search_fields = ['name', 'slug']
    readonly_fields = ['created_at']
    ordering = ['order']
    prepopulated_fields = {'slug': ('name',)}

    def feature_count(self, obj):
        return len(obj.features) if obj.features else 0
    feature_count.short_description = 'Features'


class SeoContentBlockInline(admin.TabularInline):
    model = SeoContentBlock
    extra = 1
    fields = ['key', 'content', 'order', 'is_active']
    ordering = ['order']


@admin.register(SeoPage)
class SeoPageAdmin(admin.ModelAdmin):
    list_display = [
        'meta_title_display', 'country', 'language', 'page_type', 
        'plan_badge', 'robots_badge', 'sitemap_badge', 'published_badge', 'updated_at'
    ]
    list_filter = [
        'page_type', 'plan', 'country', 'language', 
        'is_published', 'robots', 'sitemap_include'
    ]
    search_fields = ['meta_title', 'meta_description', 'h1', 'slug']
    readonly_fields = ['created_at', 'updated_at', 'canonical_url']
    prepopulated_fields = {'slug': ('h1',)}
    inlines = [SeoContentBlockInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('country', 'language', 'page_type', 'plan', 'slug')
        }),
        ('Basic SEO (All Plans)', {
            'fields': (
                'meta_title', 'meta_description', 'h1', 'h2',
                'canonical_url', 'robots', 'image_alt_fallback'
            )
        }),
        ('Growth Features', {
            'fields': (
                'keywords_hint', 'internal_links', 'sitemap_include',
                'og_title', 'og_description', 'og_image_url',
                'twitter_card', 'twitter_image_url'
            ),
            'classes': ('collapse',)
        }),
        ('Premium Features', {
            'fields': (
                'json_ld', 'breadcrumbs', 
                'local_business_schema', 'service_schema'
            ),
            'classes': ('collapse',)
        }),
        ('Publishing', {
            'fields': ('is_published', 'publish_at', 'updated_by')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['publish_pages', 'unpublish_pages', 'set_basic_plan', 'set_growth_plan', 'set_premium_plan']
    
    def meta_title_display(self, obj):
        length = len(obj.meta_title)
        color = 'green' if length <= 60 else 'red'
        return format_html(
            '<span style="color: {}">{} <small>({})</small></span>',
            color, obj.meta_title, length
        )
    meta_title_display.short_description = 'Title'
    
    def plan_badge(self, obj):
        colors = {'basic': 'blue', 'growth': 'orange', 'premium': 'purple'}
        color = colors.get(obj.plan.name, 'gray')
        return format_html(
            '<span style="background: {}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.plan.name.upper()
        )
    plan_badge.short_description = 'Plan'
    
    def robots_badge(self, obj):
        color = 'green' if 'index' in obj.robots else 'red'
        return format_html(
            '<span style="color: {}">{}</span>',
            color, obj.robots
        )
    robots_badge.short_description = 'Robots'
    
    def sitemap_badge(self, obj):
        if obj.sitemap_include:
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')
    sitemap_badge.short_description = 'Sitemap'
    
    def published_badge(self, obj):
        if obj.is_published:
            return format_html('<span style="color: green;">Published</span>')
        return format_html('<span style="color: gray;">Draft</span>')
    published_badge.short_description = 'Status'
    
    # Bulk actions
    def publish_pages(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f'{count} pages were successfully published.')
    publish_pages.short_description = 'Publish selected pages'
    
    def unpublish_pages(self, request, queryset):
        count = queryset.update(is_published=False)
        self.message_user(request, f'{count} pages were successfully unpublished.')
    unpublish_pages.short_description = 'Unpublish selected pages'
    
    def set_basic_plan(self, request, queryset):
        try:
            basic_plan = SeoPlan.objects.get(name='basic')
            count = queryset.update(plan=basic_plan)
            self.message_user(request, f'{count} pages updated to Basic plan.')
        except SeoPlan.DoesNotExist:
            self.message_user(request, 'Basic plan not found. Run seo_seed command first.', level='ERROR')
    set_basic_plan.short_description = 'Set to Basic plan'
    
    def set_growth_plan(self, request, queryset):
        try:
            growth_plan = SeoPlan.objects.get(name='growth')
            count = queryset.update(plan=growth_plan)
            self.message_user(request, f'{count} pages updated to Growth plan.')
        except SeoPlan.DoesNotExist:
            self.message_user(request, 'Growth plan not found. Run seo_seed command first.', level='ERROR')
    set_growth_plan.short_description = 'Set to Growth plan'
    
    def set_premium_plan(self, request, queryset):
        try:
            premium_plan = SeoPlan.objects.get(name='premium')
            count = queryset.update(plan=premium_plan)
            self.message_user(request, f'{count} pages updated to Premium plan.')
        except SeoPlan.DoesNotExist:
            self.message_user(request, 'Premium plan not found. Run seo_seed command first.', level='ERROR')
    set_premium_plan.short_description = 'Set to Premium plan'

    def save_model(self, request, obj, form, change):
        if not change:  # Creating new object
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(SeoContentBlock)
class SeoContentBlockAdmin(admin.ModelAdmin):
    list_display = ['seo_page', 'key', 'order', 'is_active']
    list_filter = ['is_active', 'seo_page__page_type']
    search_fields = ['key', 'content', 'seo_page__meta_title']
    ordering = ['seo_page', 'order']
