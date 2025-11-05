from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.urls import reverse, path
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, JsonResponse
from django import forms
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.conf import settings

from .models import (
    Tag, ArticleCategory, Article, ArticleBusinessFeature,
    TravelItinerary, ItineraryDay, ItineraryStop, ArticleView
)
from .magicai_integration import MagicAIClient


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_preview', 'article_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    def color_preview(self, obj):
        return format_html(
            '<span style="display: inline-block; width: 20px; height: 20px; '
            'background-color: {}; border-radius: 3px; border: 1px solid #ccc;"></span>',
            obj.color
        )
    color_preview.short_description = 'Color'
    
    def article_count(self, obj):
        return obj.article_set.count()
    article_count.short_description = 'Articles'


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon_preview', 'color_preview', 'article_count', 'is_active', 'sort_order']
    list_filter = ['is_active', 'parent', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['sort_order', 'name']
    
    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<span style="font-size: 18px;">{}</span>', obj.icon)
        return '-'
    icon_preview.short_description = 'Icon'
    
    def color_preview(self, obj):
        return format_html(
            '<span style="display: inline-block; width: 20px; height: 20px; '
            'background-color: {}; border-radius: 3px; border: 1px solid #ccc;"></span>',
            obj.color
        )
    color_preview.short_description = 'Color'
    
    def article_count(self, obj):
        return obj.article_set.count()
    article_count.short_description = 'Articles'


class ArticleBusinessFeatureInline(admin.TabularInline):
    model = ArticleBusinessFeature
    extra = 0
    autocomplete_fields = ['business']
    fields = ['business', 'description', 'sort_order']


class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'article_type', 'status', 'author', 'featured', 
        'view_count', 'cities_list', 'published_at', 'created_at'
    ]
    list_filter = [
        'status', 'article_type', 'featured', 'category',
        'countries', 'created_at', 'published_at'
    ]
    search_fields = ['title', 'subtitle', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags', 'countries', 'cities']
    inlines = [ArticleBusinessFeatureInline]
    
    fieldsets = [
        ('Content', {
            'fields': ['title', 'slug', 'subtitle', 'excerpt', 'content']
        }),
        ('Media', {
            'fields': ['featured_image', 'featured_image_alt']
        }),
        ('Classification', {
            'fields': ['article_type', 'category', 'tags', 'featured']
        }),
        ('Location', {
            'fields': ['countries', 'cities'],
            'description': 'Associate this article with specific locations'
        }),
        ('Publishing', {
            'fields': ['status', 'author', 'published_at']
        }),
        ('SEO', {
            'fields': ['meta_title', 'meta_description'],
            'classes': ['collapse']
        }),
        ('Analytics', {
            'fields': ['view_count'],
            'classes': ['collapse']
        })
    ]
    
    readonly_fields = ['view_count']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'author', 'category'
        ).prefetch_related('cities', 'countries', 'tags')
    
    def cities_list(self, obj):
        cities = obj.cities.all()[:3]
        city_names = [city.name for city in cities]
        if obj.cities.count() > 3:
            city_names.append(f"... +{obj.cities.count() - 3} more")
        return ', '.join(city_names) if city_names else '-'
    cities_list.short_description = 'Cities'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new article
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    actions = ['publish_articles', 'unpublish_articles', 'mark_as_featured', 'generate_with_magicai']
    
    def publish_articles(self, request, queryset):
        updated = queryset.filter(status='review').update(
            status='published',
            published_at=timezone.now()
        )
        self.message_user(request, f'{updated} articles published successfully.')
    publish_articles.short_description = "Publish selected articles"
    
    def unpublish_articles(self, request, queryset):
        updated = queryset.update(status='draft', published_at=None)
        self.message_user(request, f'{updated} articles unpublished.')
    unpublish_articles.short_description = "Unpublish selected articles"
    
    def mark_as_featured(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, f'{updated} articles marked as featured.')
    mark_as_featured.short_description = "Mark as featured"
    
    def generate_with_magicai(self, request, queryset):
        """Generate content for selected articles using MagicAI"""
        if not getattr(settings, 'MAGICAI_ENABLED', False):
            self.message_user(request, 'MagicAI integration is not enabled.', level=messages.WARNING)
            return
            
        client = MagicAIClient()
        generated_count = 0
        
        for article in queryset:
            if article.content and article.content.strip():
                continue  # Skip articles that already have content
                
            try:
                # Determine city name for content generation
                city_name = "European City"  # Default
                if article.cities.exists():
                    city_name = article.cities.first().name
                elif "Hamburg" in article.title:
                    city_name = "Hamburg"
                elif "Barcelona" in article.title:
                    city_name = "Barcelona"
                # Add more city detection logic as needed
                
                result = client.generate_city_guide(
                    city_name=city_name,
                    country="Europe",
                    language='en'
                )
                
                if result.get('success'):
                    article.content = result.get('content', '')
                    if not article.excerpt:
                        article.excerpt = result.get('content', '')[:200] + '...'
                    if not article.meta_description:
                        article.meta_description = result.get('content', '')[:160] + '...'
                    article.save()
                    generated_count += 1
                    
            except Exception as e:
                messages.error(request, f'Error generating content for {article.title}: {str(e)}')
        
        if generated_count > 0:
            self.message_user(request, f'Generated content for {generated_count} articles using MagicAI.')
        else:
            self.message_user(request, 'No content was generated. Articles may already have content.', level=messages.INFO)
    
    generate_with_magicai.short_description = "🤖 Generate content with MagicAI"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('magicai-generate/', self.admin_site.admin_view(self.magicai_generate_view), name='travel_article_magicai_generate'),
        ]
        return custom_urls + urls
    
    def magicai_generate_view(self, request):
        """AJAX view for generating content with MagicAI"""
        if not request.is_ajax() or request.method != 'POST':
            return JsonResponse({'error': 'Invalid request'}, status=400)
            
        if not getattr(settings, 'MAGICAI_ENABLED', False):
            return JsonResponse({'error': 'MagicAI integration is not enabled'}, status=400)
        
        article_id = request.POST.get('article_id')
        prompt_type = request.POST.get('prompt_type', 'city_guide')
        
        try:
            article = Article.objects.get(id=article_id)
            client = MagicAIClient()
            
            # Generate content based on type
            if prompt_type == 'city_guide':
                city_name = "European City"
                if article.cities.exists():
                    city_name = article.cities.first().name
                
                result = client.generate_city_guide(
                    city_name=city_name,
                    country="Europe",
                    language='en'
                )
            elif prompt_type == 'attraction':
                result = client.generate_attraction_content(
                    attraction_name=article.title,
                    city="European City",
                    attraction_type="Tourist Attraction"
                )
            else:
                return JsonResponse({'error': 'Invalid prompt type'}, status=400)
            
            if result.get('success'):
                return JsonResponse({
                    'success': True,
                    'title': result.get('title', ''),
                    'content': result.get('content', ''),
                    'excerpt': result.get('content', '')[:200] + '...',
                    'meta_description': result.get('content', '')[:160] + '...'
                })
            else:
                return JsonResponse({'error': result.get('error', 'Generation failed')}, status=400)
                
        except Article.DoesNotExist:
            return JsonResponse({'error': 'Article not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    class Media:
        js = ('travel/admin/magicai_integration.js',)
        css = {
            'all': ('travel/admin/magicai_integration.css',)
        }


class ItineraryStopInline(admin.TabularInline):
    model = ItineraryStop
    extra = 0
    autocomplete_fields = ['business']
    fields = ['title', 'business', 'time_slot', 'duration_minutes', 'estimated_cost', 'sort_order']


class ItineraryDayInline(admin.StackedInline):
    model = ItineraryDay
    extra = 0
    fields = ['day_number', 'title', 'description']


class TravelItineraryAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'city', 'duration_display', 'total_cost_estimate', 
        'is_published', 'featured', 'view_count', 'author', 'created_at'
    ]
    list_filter = ['is_published', 'featured', 'duration_type', 'city__country', 'created_at']
    search_fields = ['title', 'description', 'city__name']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ItineraryDayInline]
    
    fieldsets = [
        ('Basic Information', {
            'fields': ['title', 'slug', 'description', 'city']
        }),
        ('Duration & Cost', {
            'fields': ['duration_type', 'custom_duration_days', 'total_cost_estimate']
        }),
        ('Media', {
            'fields': ['featured_image']
        }),
        ('Publishing', {
            'fields': ['is_published', 'featured', 'author']
        }),
        ('Analytics', {
            'fields': ['view_count'],
            'classes': ['collapse']
        })
    ]
    
    readonly_fields = ['view_count']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    actions = ['publish_itineraries', 'mark_as_featured']
    
    def publish_itineraries(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} itineraries published.')
    publish_itineraries.short_description = "Publish selected itineraries"
    
    def mark_as_featured(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, f'{updated} itineraries marked as featured.')
    mark_as_featured.short_description = "Mark as featured"


class ItineraryDayAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'itinerary', 'day_number', 'stop_count']
    list_filter = ['itinerary__city', 'itinerary__is_published']
    search_fields = ['title', 'description', 'itinerary__title']
    inlines = [ItineraryStopInline]
    
    def stop_count(self, obj):
        return obj.stops.count()
    stop_count.short_description = 'Stops'


class ItineraryStopAdmin(admin.ModelAdmin):
    list_display = [
        '__str__', 'business', 'time_slot', 'duration_minutes', 
        'estimated_cost', 'sort_order'
    ]
    list_filter = ['time_slot', 'day__itinerary__city']
    search_fields = ['title', 'description', 'business__name']
    autocomplete_fields = ['business']


class ArticleViewAdmin(admin.ModelAdmin):
    list_display = ['article', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at', 'article__status']
    search_fields = ['article__title', 'ip_address']
    readonly_fields = ['article', 'ip_address', 'user_agent', 'referrer', 'viewed_at']
    
    def has_add_permission(self, request):
        return False  # Views are created automatically
    
    def has_change_permission(self, request, obj=None):
        return False  # Views shouldn't be modified


# Import the custom admin site from businesses app
from businesses.admin import admin_site

# Register travel models with the custom admin site ONLY
admin_site.register(Tag, TagAdmin)
admin_site.register(ArticleCategory, ArticleCategoryAdmin) 
admin_site.register(Article, ArticleAdmin)
admin_site.register(TravelItinerary, TravelItineraryAdmin)
admin_site.register(ItineraryDay, ItineraryDayAdmin)
admin_site.register(ItineraryStop, ItineraryStopAdmin)
admin_site.register(ArticleView, ArticleViewAdmin)