from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html

# Update the admin site to add a counter dashboard link
admin.site.site_header = "ListAcrossEU Admin"
admin.site.site_title = "ListAcrossEU Admin Portal"
admin.site.index_title = "Welcome to ListAcrossEU Administration"

# Add custom admin URLs
def get_admin_urls():
    from counters.admin import CounterRebuildLogAdmin
    counter_admin = CounterRebuildLogAdmin(model=None, admin_site=admin.site)
    return [
        path('counters/dashboard/', counter_admin.dashboard_view, name='counters_dashboard'),
    ]

# Monkey patch to add our custom URLs
original_get_urls = admin.site.get_urls

def patched_get_urls():
    urls = original_get_urls()
    custom_urls = get_admin_urls()
    return custom_urls + urls

admin.site.get_urls = patched_get_urls