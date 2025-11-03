from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from .models import BlogPost, PricingPlan, BlogCategory
from catalog.models import Business, Category
from geo.models import Country


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'language', 'status', 'featured', 'published_at', 'view_count', 'read_time']
    list_filter = ['status', 'language', 'featured', 'category', 'published_at', 'created_at']
    search_fields = ['title', 'excerpt', 'author__username', 'author__first_name', 'author__last_name', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ['-published_at', '-created_at']
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'language'),
            'description': 'Essential post information and identification'
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'image', 'image_alt'),
            'description': 'Main post content and media'
        }),
        ('Categorization', {
            'fields': ('category', 'tags'),
            'description': 'Organization and tagging'
        }),
        ('Publishing', {
            'fields': ('status', 'featured', 'published_at'),
            'description': 'Publication settings and visibility'
        }),
        ('SEO & Metadata', {
            'fields': ('meta_title', 'meta_description', 'read_time'),
            'classes': ('collapse',),
            'description': 'Search engine optimization and metadata'
        }),
        ('Analytics', {
            'fields': ('view_count', 'created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Performance metrics and timestamps'
        })
    )
    
    readonly_fields = ['view_count', 'created_at', 'updated_at', 'read_time']
    
    actions = ['publish_posts', 'unpublish_posts', 'feature_posts', 'unfeature_posts']
    
    def publish_posts(self, request, queryset):
        updated = queryset.update(status='published', published_at=timezone.now())
        self.message_user(request, f'{updated} posts published successfully.')
    publish_posts.short_description = "Publish selected posts"
    
    def unpublish_posts(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} posts moved to draft.')
    unpublish_posts.short_description = "Move selected posts to draft"
    
    def feature_posts(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, f'{updated} posts marked as featured.')
    feature_posts.short_description = "Mark selected posts as featured"
    
    def unfeature_posts(self, request, queryset):
        updated = queryset.update(featured=False)
        self.message_user(request, f'{updated} posts removed from featured.')
    unfeature_posts.short_description = "Remove featured status from selected posts"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category')
    
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'currency', 'billing_cycle', 'is_active', 'is_featured', 'order']
    list_filter = ['is_active', 'is_featured', 'billing_cycle', 'currency']
    search_fields = ['name', 'description', 'features']
    ordering = ['order', 'price']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'order')
        }),
        ('Pricing', {
            'fields': ('price', 'currency', 'billing_cycle', 'trial_days')
        }),
        ('Features', {
            'fields': ('features', 'max_listings', 'max_images', 'priority_support')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'is_featured', 'color_scheme')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at', 'updated_at']


class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'country', 'status', 'created_at']
    list_filter = ['status', 'country', 'created_at']
    search_fields = ['name', 'city__name', 'street', 'phone', 'email']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug')
        }),
        ('Location', {
            'fields': ('street', 'city', 'town', 'postcode', 'country', 'lat', 'lng')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'website')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['activate_businesses', 'deactivate_businesses']
    
    def activate_businesses(self, request, queryset):
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} businesses activated successfully.')
    activate_businesses.short_description = "Activate selected businesses"
    
    def deactivate_businesses(self, request, queryset):
        updated = queryset.update(status='inactive')
        self.message_user(request, f'{updated} businesses deactivated.')
    deactivate_businesses.short_description = "Deactivate selected businesses"


class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'active', 'get_color_display', 'post_count']
    list_filter = ['active', 'created_at']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Display Settings', {
            'fields': ('color', 'active')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at']
    
    def get_color_display(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc; border-radius: 3px;"></div>',
            obj.color
        )
    get_color_display.short_description = 'Color'
    
    def post_count(self, obj):
        return obj.blogpost_set.count()
    post_count.short_description = 'Posts'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['slug', 'get_english_name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['slug', 'names_json']
    
    def get_english_name(self, obj):
        return obj.get_name('en')
    get_english_name.short_description = 'English Name'
    

class AdminDashboardView:
    """Custom admin dashboard with statistics and quick actions"""
    
    def dashboard_view(self, request):
        from django.db.models import Count, Q
        from datetime import datetime, timedelta
        
        # Get statistics
        stats = {
            'total_businesses': Business.objects.count(),
            'verified_businesses': Business.objects.filter(verified=True).count(),
            'featured_businesses': Business.objects.filter(featured=True).count(),
            'total_blog_posts': BlogPost.objects.count(),
            'published_posts': BlogPost.objects.filter(status='published').count(),
            'total_categories': Category.objects.count(),
            'active_pricing_plans': PricingPlan.objects.filter(is_active=True).count(),
        }
        
        # Recent activity
        recent_businesses = Business.objects.order_by('-created_at')[:5]
        recent_blog_posts = BlogPost.objects.order_by('-published_at')[:5]
        
        # Monthly stats
        thirty_days_ago = datetime.now() - timedelta(days=30)
        monthly_stats = {
            'new_businesses': Business.objects.filter(created_at__gte=thirty_days_ago).count(),
            'new_blog_posts': BlogPost.objects.filter(published_at__gte=thirty_days_ago).count(),
        }
        
        context = {
            'title': 'ListAcrossEU Admin Dashboard',
            'stats': stats,
            'monthly_stats': monthly_stats,
            'recent_businesses': recent_businesses,
            'recent_blog_posts': recent_blog_posts,
        }
        
        return render(request, 'admin/dashboard.html', context)


# Register blog models
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)
admin.site.register(PricingPlan, PricingPlanAdmin)

# Override existing registrations if they exist
try:
    admin.site.unregister(Business)
    admin.site.unregister(Category)
except admin.sites.NotRegistered:
    pass

admin.site.register(Business, BusinessAdmin)
admin.site.register(Category, CategoryAdmin)

# Customize admin site
admin.site.site_header = 'ListAcrossEU Administration'
admin.site.site_title = 'ListAcrossEU Admin'
admin.site.index_title = 'Welcome to ListAcrossEU Administration'