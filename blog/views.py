from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Category, Post
from .serializers import CategorySerializer, PostCardSerializer, PostDetailSerializer


class CategoryList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostList(ListAPIView):
    serializer_class = PostCardSerializer
    
    def get_queryset(self):
        lang = self.request.query_params.get("lang", "en")
        category = self.request.query_params.get("category")
        featured = self.request.query_params.get("featured")
        q = self.request.query_params.get("q")
        
        qs = Post.objects.filter(is_published=True, language=lang)
        
        if category:
            qs = qs.filter(category__slug=category)
        
        if featured == "true":
            qs = qs.filter(is_featured=True)
            
        if q:
            qs = qs.filter(title__icontains=q)
        
        # Weighted sort by plan/featured, then recency
        posts = list(qs.select_related("category", "author", "visibility__plan"))
        posts.sort(key=lambda p: (p.list_weight(), p.published_at or p.created_at), reverse=True)
        return posts


class PostDetail(RetrieveAPIView):
    serializer_class = PostDetailSerializer
    lookup_field = "slug"
    
    def get_object(self):
        slug = self.kwargs["slug"]
        lang = self.kwargs.get("lang", "en")
        return get_object_or_404(
            Post.objects.select_related("category", "author").prefetch_related("related_posts"),
            slug=slug, 
            language=lang, 
            is_published=True
        )


@api_view(["GET"])
def post_search(request):
    """Search posts by title and content"""
    query = request.GET.get("q", "")
    lang = request.GET.get("lang", "en")
    
    if not query:
        return Response({"results": []})
    
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(excerpt__icontains=query) | Q(content__icontains=query),
        language=lang,
        is_published=True
    ).select_related("category", "author")[:20]
    
    serializer = PostCardSerializer(posts, many=True)
    return Response({"results": serializer.data})


@api_view(["GET"])
def featured_posts(request):
    """Get featured posts for homepage"""
    lang = request.GET.get("lang", "en")
    
    posts = Post.objects.filter(
        language=lang,
        is_published=True,
        is_featured=True
    ).select_related("category", "author")[:6]
    
    serializer = PostCardSerializer(posts, many=True)
    return Response({"posts": serializer.data})
