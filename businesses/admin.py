from django.contrib import admin
from .models import Business, Category, Country, City, Review, BusinessImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'sort_order']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['sort_order', 'name']


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_eu_member', 'is_active']
    list_filter = ['is_eu_member', 'is_active']
    search_fields = ['name', 'code']
    ordering = ['name']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'population', 'is_capital']
    list_filter = ['country', 'is_capital']
    search_fields = ['name', 'country__name']
    ordering = ['country__name', 'name']


class BusinessImageInline(admin.TabularInline):
    model = BusinessImage
    extra = 1


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'owner', 'city', 'category', 'plan', 'status',
        'featured', 'verified', 'created_at'
    ]
    list_filter = [
        'plan', 'status', 'featured', 'verified', 'category',
        'city__country', 'created_at'
    ]
    search_fields = ['name', 'email', 'owner__email', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['id', 'views_count', 'clicks_count', 'created_at', 'updated_at']
    
    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'slug', 'owner', 'description', 'short_description']
        }),
        ('Contact Information', {
            'fields': ['email', 'phone', 'website']
        }),
        ('Location', {
            'fields': ['address', 'city', 'postal_code', 'latitude', 'longitude']
        }),
        ('Categories', {
            'fields': ['category', 'subcategories']
        }),
        ('Media', {
            'fields': ['logo', 'cover_image']
        }),
        ('Business Hours', {
            'fields': [
                'monday_hours', 'tuesday_hours', 'wednesday_hours',
                'thursday_hours', 'friday_hours', 'saturday_hours', 'sunday_hours'
            ],
            'classes': ['collapse']
        }),
        ('Subscription & Status', {
            'fields': ['plan', 'status', 'featured', 'verified']
        }),
        ('SEO', {
            'fields': ['meta_title', 'meta_description', 'keywords'],
            'classes': ['collapse']
        }),
        ('Statistics', {
            'fields': ['views_count', 'clicks_count'],
            'classes': ['collapse']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at', 'published_at', 'expires_at'],
            'classes': ['collapse']
        })
    ]
    
    inlines = [BusinessImageInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('owner', 'city', 'category')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'business', 'reviewer', 'rating', 'is_approved', 'created_at'
    ]
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['business__name', 'reviewer__email', 'title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = [
        ('Review Information', {
            'fields': ['business', 'reviewer', 'rating', 'title', 'content']
        }),
        ('Moderation', {
            'fields': ['is_approved', 'moderation_notes']
        }),
        ('Business Response', {
            'fields': ['owner_response', 'response_date']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at']
        })
    ]