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
from blog.views import (BlogPosts, BlogPostDetail, BlogFeatured, BlogPostsAdmin, CategoryList,
                       ai_generate_outline, ai_generate_draft, ai_generate_seo, ai_translate_article,
                       admin_ai_generate_outline, admin_ai_generate_draft, admin_ai_generate_seo, 
                       admin_create_post_from_ai, admin_publish_post)
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
    path("api/v1/blog/categories/", CategoryList.as_view(), name="blog_categories"),
    path("api/v1/blog/posts/", BlogPosts.as_view(), name="blog_posts"),
    path("api/v1/blog/posts/featured/", BlogFeatured.as_view(), name="blog_featured"),
    path("api/v1/blog/posts/<slug:slug>/", BlogPostDetail.as_view(), name="blog_post_detail"),
    
    # Admin Blog API endpoints
    path("api/v1/admin/blog/posts/", BlogPostsAdmin.as_view(), name="admin_blog_posts"),
    path("api/v1/admin/blog/posts/<int:post_id>/", BlogPostsAdmin.as_view(), name="admin_blog_post_detail"),
    
    # Blog AI Generation endpoints (legacy paths for compatibility)
    path("api/v1/blog/ai/outline/", ai_generate_outline, name="blog_ai_outline"),
    path("api/v1/blog/ai/draft/", ai_generate_draft, name="blog_ai_draft"),
    path("api/v1/blog/ai/seo/", ai_generate_seo, name="blog_ai_seo"),
    path("api/v1/blog/ai/translate/", ai_translate_article, name="blog_ai_translate"),
    
    # Admin AI Generation Flow (complete post creation workflow)
    path("api/v1/ai/generate/outline/", admin_ai_generate_outline, name="admin_ai_generate_outline"),
    path("api/v1/ai/generate/draft/", admin_ai_generate_draft, name="admin_ai_generate_draft"),
    path("api/v1/ai/generate/seo/", admin_ai_generate_seo, name="admin_ai_generate_seo"),
    path("api/v1/posts/", admin_create_post_from_ai, name="admin_create_post_from_ai"),
    path("api/v1/posts/<int:post_id>/publish/", admin_publish_post, name="admin_publish_post"),
    
    # Blog AI API endpoints (new service)
    path("api/v1/blog/ai/", include('blog_ai.urls')),
    
    # Featured businesses endpoint
    path("api/v1/featured/", FeaturedBusinesses.as_view(), name="featured_businesses"),
    
    # Admin API endpoints
    path("api/v1/dashboard/stats/", dashboard_stats, name="dashboard_stats"),
    path("api/v1/csrf-token/", csrf_token, name="csrf_token"),
    path("api/v1/admin/health/", admin_health_check, name="admin_health_check"),
    
    # Core settings API
    path("api/v1/core/", include("core.urls")),
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