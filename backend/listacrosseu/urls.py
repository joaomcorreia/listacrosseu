"""
URL configuration for listacrosseu project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

def root_view(request):
    """Root endpoint that provides API information"""
    return JsonResponse({
        'message': 'Welcome to ListAcrossEU API',
        'endpoints': {
            'admin': '/admin/',
            'api': {
                'categories': '/api/categories/',
                'countries': '/api/countries/',
                'cities': '/api/cities/',
                'towns': '/api/towns/',
                'businesses': '/api/businesses/',
                'assistant': '/api/assistant/live',
            }
        },
        'status': 'running'
    })

def admin_dashboard_view(request):
    """Custom admin dashboard"""
    from blog.admin import AdminDashboardView
    dashboard = AdminDashboardView()
    return dashboard.dashboard_view(request)

urlpatterns = [
    path('', root_view, name='root'),
    path('admin/', admin.site.urls),
    path('admin/dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('api/', include('api.urls')),
    path('api/site-settings/', include('site_settings.urls')),
    path('blog/', include('blog.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('assistant_studio.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)