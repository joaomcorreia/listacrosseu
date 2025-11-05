"""listacrosseu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from businesses.sitemaps import sitemaps as business_sitemaps
from core.sitemaps import PageSitemap, PostSitemap
from businesses.admin import admin_site
from assist.views import AISuggest
from plans.views import PlanList

urlpatterns = [
    path('admin/', admin_site.urls),
    
    # Travel guides (main feature)
    path('', include('travel.urls')),
    
    # Business directory
    path('directory/', include('businesses.urls')),
    
    # Listy AI Assistant
    path('listy/', include('chatbot.urls')),
    
    # API endpoints
    path('api/v1/', include('businesses.api_urls')),
    path('api/v1/cms/', include('cms.urls')),
    path('api/v1/blog/', include('blog.urls')),
    path('api/ai/suggest/', AISuggest.as_view(), name='api-ai-suggest'),
    path('api/plans/', PlanList.as_view(), name='api-plans'),
    
    # SEO module
    path('seo/', include('seo.urls')),
    path('api/seo/', include(('seo.urls', 'seo'), namespace='seo-api')),
    
    # SEO URLs
    path('sitemap.xml', sitemap, {'sitemaps': {**business_sitemaps, "pages": PageSitemap, "posts": PostSitemap}}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)