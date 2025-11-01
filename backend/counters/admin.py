from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.html import format_html
from .models import CategoryCountry, CategoryCountryCity, CategoryCityTown, CounterRebuildLog


@admin.register(CategoryCountry)
class CategoryCountryAdmin(admin.ModelAdmin):
    list_display = ['category', 'country', 'business_count']
    list_filter = ['category', 'country']
    search_fields = ['category__slug', 'country__code']
    ordering = ['-business_count']


@admin.register(CategoryCountryCity)
class CategoryCountryCityAdmin(admin.ModelAdmin):
    list_display = ['category', 'country', 'city', 'business_count']
    list_filter = ['category', 'country', 'city']
    search_fields = ['category__slug', 'country__code', 'city__name']
    ordering = ['-business_count']


@admin.register(CategoryCityTown)
class CategoryCityTownAdmin(admin.ModelAdmin):
    list_display = ['category', 'city', 'town', 'business_count']
    list_filter = ['category', 'city']
    search_fields = ['category__slug', 'city__name', 'town__name']
    ordering = ['-business_count']


@admin.register(CounterRebuildLog)
class CounterRebuildLogAdmin(admin.ModelAdmin):
    list_display = ['rebuilt_at', 'rebuild_type', 'notes']
    list_filter = ['rebuild_type', 'rebuilt_at']
    readonly_fields = ['rebuilt_at']
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.dashboard_view), name='counters_dashboard'),
            path('rebuild/', self.admin_site.admin_view(self.rebuild_view), name='counters_rebuild'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        from django.core.management import call_command
        from io import StringIO
        
        context = {
            'title': 'Counter Dashboard',
            'last_rebuild': CounterRebuildLog.objects.first(),
            'category_country_count': CategoryCountry.objects.count(),
            'category_country_city_count': CategoryCountryCity.objects.count(),
            'category_city_town_count': CategoryCityTown.objects.count(),
        }
        
        if request.method == 'POST':
            action = request.POST.get('action')
            try:
                if action == 'rebuild_all':
                    call_command('rebuild_counters')
                    messages.success(request, 'All counters rebuilt successfully')
                elif action == 'rebuild_category':
                    category_id = request.POST.get('category_id')
                    if category_id:
                        call_command('rebuild_counters', category=category_id)
                        messages.success(request, f'Counters for category {category_id} rebuilt successfully')
                    else:
                        messages.error(request, 'Category ID required')
            except Exception as e:
                messages.error(request, f'Error rebuilding counters: {str(e)}')
            
            return redirect('admin:counters_dashboard')
        
        return render(request, 'admin/counters_dashboard.html', context)
    
    def rebuild_view(self, request):
        # This is handled in dashboard_view
        return redirect('admin:counters_dashboard')