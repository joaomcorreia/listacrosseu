from django.contrib import admin
from .models import Category, Business, BusinessCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['slug', 'get_en_name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['slug', 'names_json']
    prepopulated_fields = {'slug': ('names_json',)}
    
    def get_en_name(self, obj):
        return obj.get_name('en')
    get_en_name.short_description = 'English Name'


class BusinessCategoryInline(admin.TabularInline):
    model = BusinessCategory
    extra = 1


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'city', 'country', 'status', 'created_at']
    list_filter = ['status', 'country', 'city', 'created_at']
    search_fields = ['name', 'slug', 'email', 'phone']
    inlines = [BusinessCategoryInline]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BusinessCategory)
class BusinessCategoryAdmin(admin.ModelAdmin):
    list_display = ['business', 'category']
    list_filter = ['category']
    search_fields = ['business__name', 'category__slug']