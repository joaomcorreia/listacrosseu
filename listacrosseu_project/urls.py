"""listacrosseu_project URL Configuration

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
from django.conf.urls.i18n import i18n_patterns
from blog.views import BlogPosts, BlogPostDetail, BlogFeatured, BlogPostsAdmin
from listings.views import FeaturedBusinesses
from .admin_api_views import dashboard_stats, csrf_token, admin_health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('listings.urls')),
    path('api/assistant/', include('assistant.urls')),
    path('accounts/', include('accounts.urls')),
    path('billing/', include('billing.urls')),
    path('seo/', include('seo.urls')),
    
    # Blog API endpoints
    path("api/v1/blog/posts/", BlogPosts.as_view(), name="blog_posts"),
    path("api/v1/blog/posts/featured/", BlogFeatured.as_view(), name="blog_featured"),
    path("api/v1/blog/posts/<slug:slug>/", BlogPostDetail.as_view(), name="blog_post_detail"),
    
    # Admin Blog API endpoints
    path("api/v1/admin/blog/posts/", BlogPostsAdmin.as_view(), name="admin_blog_posts"),
    path("api/v1/admin/blog/posts/<int:post_id>/", BlogPostsAdmin.as_view(), name="admin_blog_post_detail"),
    
    # Featured businesses endpoint
    path("api/v1/featured/", FeaturedBusinesses.as_view(), name="featured_businesses"),
    
    # Admin API endpoints
    path("api/v1/dashboard/stats/", dashboard_stats, name="dashboard_stats"),
    path("api/v1/csrf-token/", csrf_token, name="csrf_token"),
    path("api/v1/admin/health/", admin_health_check, name="admin_health_check"),
]

# Add i18n patterns for internationalized URLs
urlpatterns += i18n_patterns(
    path('', include('pages.urls')),
    prefix_default_language=False,
)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)