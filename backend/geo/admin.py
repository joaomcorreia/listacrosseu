from django.contrib import admin
from .models import Country, City, Town


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['code', 'get_en_name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['code', 'names_json']
    
    def get_en_name(self, obj):
        return obj.get_name('en')
    get_en_name.short_description = 'English Name'


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'country', 'is_active']
    list_filter = ['country', 'is_active']
    search_fields = ['name', 'slug']


@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'city', 'is_active']
    list_filter = ['city__country', 'is_active']
    search_fields = ['name', 'slug']