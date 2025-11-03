from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from .models import BlogPost, BlogCategory, PricingPlan
from .serializers import (
    BlogPostSerializer, 
    BlogPostListSerializer,
    BlogCategorySerializer, 
    PricingPlanSerializer
)
import django_filters


class BlogPostFilter(django_filters.FilterSet):
    """Custom filter for blog posts"""
    category = django_filters.CharFilter(field_name='category__slug')
    author = django_filters.CharFilter(field_name='author__username')
    featured = django_filters.BooleanFilter()
    search = django_filters.CharFilter(method='filter_search')
    tags = django_filters.CharFilter(method='filter_tags')
    
    class Meta:
        model = BlogPost
        fields = {
            'language': ['exact'],
            'status': ['exact'],
            'published_at': ['gte', 'lte'],
            'created_at': ['gte', 'lte'],
        }
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(excerpt__icontains=value) |
            Q(content__icontains=value)
        )
    
    def filter_tags(self, queryset, name, value):
        return queryset.filter(tags__icontains=value)


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for blog posts with advanced filtering and search
    """
    queryset = BlogPost.objects.filter(status='published').select_related(
        'author', 'category'
    ).order_by('-featured', '-published_at')
    
    serializer_class = BlogPostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BlogPostFilter
    search_fields = ['title', 'excerpt', 'content']
    ordering_fields = ['published_at', 'view_count', 'read_time', 'title']
    ordering = ['-featured', '-published_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BlogPostListSerializer
        return BlogPostSerializer
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured blog posts"""
        featured_posts = self.get_queryset().filter(featured=True)[:6]
        serializer = BlogPostListSerializer(featured_posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get posts grouped by category"""
        categories = BlogCategory.objects.filter(active=True).prefetch_related('blogpost_set')
        result = {}
        
        for category in categories:
            posts = category.blogpost_set.filter(
                status='published',
                language=request.GET.get('lang', 'en')
            )[:3]
            result[category.slug] = {
                'category': BlogCategorySerializer(category).data,
                'posts': BlogPostListSerializer(posts, many=True).data
            }
        
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get most popular posts by view count"""
        popular_posts = self.get_queryset().order_by('-view_count')[:10]
        serializer = BlogPostListSerializer(popular_posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get most recent posts"""
        language = request.GET.get('lang', 'en')
        limit = int(request.GET.get('limit', 5))
        
        recent_posts = self.get_queryset().filter(language=language)[:limit]
        serializer = BlogPostListSerializer(recent_posts, many=True)
        return Response(serializer.data)


class BlogCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for blog categories
    """
    queryset = BlogCategory.objects.filter(active=True).annotate(
        post_count=Count('blogpost')
    ).order_by('name')
    serializer_class = BlogCategorySerializer
    lookup_field = 'slug'
    
    @action(detail=True, methods=['get'])
    def posts(self, request, slug=None):
        """Get posts for a specific category"""
        category = self.get_object()
        language = request.GET.get('lang', 'en')
        
        posts = BlogPost.objects.filter(
            category=category,
            status='published',
            language=language
        ).select_related('author', 'category').order_by('-published_at')
        
        # Pagination
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = BlogPostListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = BlogPostListSerializer(posts, many=True)
        return Response(serializer.data)


class PricingPlanViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for pricing plans
    """
    queryset = PricingPlan.objects.filter(is_active=True).order_by('order', 'price')
    serializer_class = PricingPlanSerializer
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured pricing plans"""
        featured_plans = self.get_queryset().filter(is_featured=True)
        serializer = PricingPlanSerializer(featured_plans, many=True)
        return Response(serializer.data)