"""
URL configuration for listacrosseu project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.shortcuts import redirect

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
            }
        },
        'status': 'running'
    })

urlpatterns = [
    path('', root_view, name='root'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]