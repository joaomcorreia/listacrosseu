from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.db.models import Q, F
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import BlogPost, BlogCategory
from .serializers import BlogPostSerializer, BlogCategorySerializer


class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = BlogPost.objects.filter(status='published').select_related('category', 'author')
        
        # Language filtering
        language = self.request.GET.get('lang', 'en')
        queryset = queryset.filter(language=language)
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(content__icontains=search) |
                Q(excerpt__icontains=search)
            )
        
        # Category filtering
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        return queryset.order_by('-featured', '-published_at')


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return BlogPost.objects.filter(status='published').select_related('category', 'author')
    
    def get_object(self):
        post = super().get_object()
        # Increment view count
        BlogPost.objects.filter(pk=post.pk).update(view_count=F('view_count') + 1)
        return post


class BlogCategoryView(ListView):
    model = BlogPost
    template_name = 'blog/category.html'
    context_object_name = 'posts'
    paginate_by = 12
    
    def get_queryset(self):
        self.category = get_object_or_404(BlogCategory, slug=self.kwargs['category_slug'])
        language = self.request.GET.get('lang', 'en')
        return BlogPost.objects.filter(
            category=self.category,
            language=language,
            status='published'
        ).select_related('category', 'author').order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class BlogTagView(ListView):
    model = BlogPost
    template_name = 'blog/tag.html'
    context_object_name = 'posts'
    paginate_by = 12
    
    def get_queryset(self):
        self.tag = self.kwargs['tag']
        language = self.request.GET.get('lang', 'en')
        return BlogPost.objects.filter(
            tags__icontains=self.tag,
            language=language,
            status='published'
        ).select_related('category', 'author').order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


# API Views for frontend integration
@api_view(['GET'])
def blog_posts_api(request):
    """API endpoint for blog posts with filtering and pagination"""
    language = request.GET.get('lang', 'en')
    featured = request.GET.get('featured')
    category = request.GET.get('category')
    limit = int(request.GET.get('limit', 10))
    
    queryset = BlogPost.objects.filter(
        status='published',
        language=language
    ).select_related('category', 'author')
    
    if featured:
        queryset = queryset.filter(featured=True)
    
    if category:
        queryset = queryset.filter(category__slug=category)
    
    posts = queryset.order_by('-featured', '-published_at')[:limit]
    serializer = BlogPostSerializer(posts, many=True)
    
    return Response({
        'posts': serializer.data,
        'total': queryset.count()
    })


@api_view(['GET'])
def blog_categories_api(request):
    """API endpoint for blog categories"""
    categories = BlogCategory.objects.filter(active=True).order_by('name')
    serializer = BlogCategorySerializer(categories, many=True)
    
    return Response({
        'categories': serializer.data
    })


@api_view(['GET'])
def blog_post_detail_api(request, slug):
    """API endpoint for single blog post"""
    try:
        post = BlogPost.objects.select_related('category', 'author').get(
            slug=slug, 
            status='published'
        )
        # Increment view count
        BlogPost.objects.filter(pk=post.pk).update(view_count=F('view_count') + 1)
        
        serializer = BlogPostSerializer(post)
        return Response(serializer.data)
    except BlogPost.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)