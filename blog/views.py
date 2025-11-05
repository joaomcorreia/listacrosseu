from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from .models import BlogPost
from .serializers import BlogPostListSerializer, BlogPostDetailSerializer


class BlogPosts(APIView):
    """List published blog posts"""
    
    def get(self, request):
        limit = int(request.GET.get("limit", 12))
        lang = request.GET.get("lang", "en")
        qs = BlogPost.objects.filter(
            status='published',
            published_at__lte=timezone.now()
        ).order_by("-published_at")[:limit]
        
        serializer = BlogPostListSerializer(qs, many=True, context={'lang': lang})
        return Response({
            "results": serializer.data
        })


class BlogFeatured(APIView):
    """List featured published blog posts"""
    
    def get(self, request):
        limit = int(request.GET.get("limit", 6))
        lang = request.GET.get("lang", "en")
        qs = BlogPost.objects.filter(
            status='published',
            is_featured=True,
            published_at__lte=timezone.now()
        ).order_by("-published_at")[:limit]
        
        serializer = BlogPostListSerializer(qs, many=True, context={'lang': lang})
        return Response({
            "results": serializer.data
        })


class BlogPostDetail(APIView):
    """Get a single blog post by slug"""
    
    def get(self, request, slug):
        lang = request.GET.get("lang", "en")
        post = get_object_or_404(
            BlogPost,
            slug=slug,
            status='published',
            published_at__lte=timezone.now()
        )
        
        serializer = BlogPostDetailSerializer(post, context={'lang': lang})
        return Response(serializer.data)


class BlogPostsAdmin(APIView):
    """Admin API for blog posts with pagination, search, and CRUD operations"""
    
    def get(self, request):
        """List all blog posts with pagination and filtering"""
        page = int(request.GET.get('page', 1))
        search = request.GET.get('search', '')
        status_filter = request.GET.get('status', 'all')
        lang = request.GET.get('lang', 'en')
        
        # Start with all blog posts
        queryset = BlogPost.objects.all().order_by('-created_at')
        
        # Apply search filter
        if search:
            queryset = queryset.filter(
                Q(title_en__icontains=search) | 
                Q(title_fr__icontains=search) |
                Q(title_nl__icontains=search) |
                Q(title_pt__icontains=search) |
                Q(title_de__icontains=search) |
                Q(title_es__icontains=search) |
                Q(excerpt_en__icontains=search) |
                Q(excerpt_fr__icontains=search) |
                Q(excerpt_nl__icontains=search) |
                Q(excerpt_pt__icontains=search) |
                Q(excerpt_de__icontains=search) |
                Q(excerpt_es__icontains=search) |
                Q(author__first_name__icontains=search) |
                Q(author__last_name__icontains=search)
            )
        
        # Apply status filter
        if status_filter != 'all':
            queryset = queryset.filter(status=status_filter)
        
        # Paginate results
        paginator = Paginator(queryset, 10)  # 10 posts per page
        page_obj = paginator.get_page(page)
        
        # Serialize the results
        serializer = BlogPostListSerializer(page_obj.object_list, many=True, context={'lang': lang})
        
        return Response({
            'count': paginator.count,
            'next': page_obj.next_page_number() if page_obj.has_next() else None,
            'previous': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'results': serializer.data
        })
    
    def delete(self, request, post_id=None):
        """Delete a blog post"""
        if not post_id:
            return Response({'error': 'Post ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            post = BlogPost.objects.get(id=post_id)
            post.delete()
            return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except BlogPost.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = BlogPostDetailSerializer(post, context={'lang': lang})
        return Response(serializer.data)