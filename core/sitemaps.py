from django.contrib.sitemaps import Sitemap
from cms.models import Page
from blog.models import Post


class PageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6
    
    def items(self):
        return Page.objects.filter(is_published=True)
    
    def location(self, obj):
        return f"/{obj.language}/{obj.slug}/"
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def _ok(self, obj):
        if obj.visibility and not obj.visibility.include_in_sitemap:
            return False
        return not obj.noindex
    
    def get_urls(self, *a, **k):
        return super().get_urls(*a, **k)
    
    def filter(self, items):
        return [i for i in items if self._ok(i)]


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    
    def items(self):
        return Post.objects.filter(is_published=True)
    
    def location(self, obj):
        return f"/{obj.language}/blog/{obj.slug}/"
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def _ok(self, obj):
        if obj.visibility and not obj.visibility.include_in_sitemap:
            return False
        return not obj.noindex
    
    def filter(self, items):
        return [i for i in items if self._ok(i)]