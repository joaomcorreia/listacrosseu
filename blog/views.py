from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.text import slugify
from .models import BlogPost, BlogCategory, AIGeneration
from .serializers import BlogPostListSerializer, BlogPostDetailSerializer, BlogPostAdminSerializer, BlogCategorySerializer


class CategoryList(APIView):
    """List and create blog categories"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Get all blog categories"""
        lang = request.GET.get('lang', 'en')
        categories = BlogCategory.objects.filter(is_active=True).order_by('name_en')
        serializer = BlogCategorySerializer(categories, many=True, context={'lang': lang})
        return Response({
            'results': serializer.data
        })
    
    def post(self, request):
        """Create a new blog category"""
        data = request.data
        
        try:
            # Generate slug from English name
            slug = slugify(data.get('name', ''))
            if not slug:
                return Response({'error': 'Category name is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if slug already exists
            if BlogCategory.objects.filter(slug=slug).exists():
                return Response({'error': 'Category with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create the category
            category = BlogCategory.objects.create(
                name_en=data.get('name', ''),
                slug=slug,
                description_en=data.get('description', ''),
                is_active=True
            )
            
            # Update SEO fields if they exist and are provided
            if data.get('meta_title'):
                category.meta_title_en = data.get('meta_title', '')
            if data.get('meta_description'):
                category.meta_description_en = data.get('meta_description', '')
            category.save()
            
            serializer = BlogCategorySerializer(category, context={'lang': 'en'})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
    permission_classes = [AllowAny]
    
    def get(self, request, post_id=None):
        """List all blog posts with pagination and filtering, or get a specific post"""
        if post_id:
            # Get specific post
            try:
                post = BlogPost.objects.get(id=post_id)
                serializer = BlogPostAdminSerializer(post)
                return Response(serializer.data)
            except BlogPost.DoesNotExist:
                return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # List all posts with pagination and filtering
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
    
    def post(self, request):
        """Create a new blog post"""
        serializer = BlogPostAdminSerializer(data=request.data)
        if serializer.is_valid():
            # Set author to the current user if authenticated, otherwise use a default
            if request.user.is_authenticated:
                serializer.save(author=request.user)
            else:
                # For demo purposes, use the first user
                from django.contrib.auth.models import User
                author = User.objects.first()
                serializer.save(author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, post_id=None):
        """Update a blog post"""
        if not post_id:
            return Response({'error': 'Post ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            post = BlogPost.objects.get(id=post_id)
            serializer = BlogPostAdminSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BlogPost.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

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


# Direct AI provider import
from blog_ai.ai_providers import AIProviderFactory
import re
import json


def ok(data):
    """Helper to return success response"""
    return Response(data, status=status.HTTP_200_OK)


def _has_claims_needing_citation(html):
    """
    Check if HTML content contains monetary amounts or dates that require citations.
    Returns True if content has € amounts or 4-digit years that need verification.
    """
    has_money = re.search(r"€\s?\d", html) or re.search(r"\b\d{4}\b", html)
    return bool(has_money)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_generate_outline(request):
    """Generate blog post outline using AI"""
    try:
        payload = request.data
        language = payload.get("language", "en")
        topic = payload.get("topic", "")
        target_audience = payload.get("target_audience", "EU business owners")
        
        if not topic:
            return Response(
                {"error": "Topic is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Call AI provider directly
        provider = AIProviderFactory.get_provider()
        outline_data = provider.generate_outline(topic, target_audience)
        
        log = AIGeneration.objects.create(
            stage="outline", 
            language=language, 
            input_payload=payload, 
            output_payload=outline_data, 
            sources=[s.get("url", "") for s in outline_data.get("sources", [])], 
            quality_score=0.85
        )
        
        return ok({"outline": outline_data, "generation_id": str(log.id)})
        
    except Exception as e:
        return Response(
            {"error": f"Failed to generate outline: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_generate_draft(request):
    """Generate blog post draft from outline"""
    try:
        payload = request.data
        outline = payload.get("outline", "")
        word_count = payload.get("word_count", 800)
        
        if not outline:
            return Response(
                {"error": "Outline is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Call AI provider directly
        provider = AIProviderFactory.get_provider()
        draft_data = provider.generate_draft(outline, word_count)
        
        log = AIGeneration.objects.create(
            stage="draft", 
            language=payload.get("language", "en"), 
            input_payload=payload, 
            output_payload=draft_data, 
            sources=[c.get("url", "") for c in draft_data.get("citations", [])], 
            quality_score=0.88
        )
        
        return ok({"draft": draft_data, "generation_id": str(log.id)})
        
    except Exception as e:
        return Response(
            {"error": f"Failed to generate draft: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_generate_seo(request):
    """Generate SEO metadata for blog post"""
    try:
        payload = request.data
        title = payload.get("title", "")
        content = payload.get("content", "")
        target_keywords = payload.get("target_keywords", "")
        
        # Call AI provider directly
        provider = AIProviderFactory.get_provider()
        
        # Combine title and content for SEO analysis
        full_content = f"# {title}\n\n{content}" if title else content
        keywords_list = target_keywords.split(',') if isinstance(target_keywords, str) else []
        
        seo_data = provider.generate_seo(full_content, keywords_list)
        
        AIGeneration.objects.create(
            stage="seo", 
            language=payload.get("language", "en"), 
            input_payload=payload, 
            output_payload=seo_data, 
            sources=[], 
            quality_score=0.9
        )
        
        return ok({"seo": seo_data})
        
    except Exception as e:
        return Response(
            {"error": f"Failed to generate SEO: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_translate_article(request):
    """Translate blog post content to target language"""
    try:
        payload = request.data
        content = payload.get("content", "")
        target_language = payload.get("target_language", "")
        
        if not content or not target_language:
            return Response(
                {"error": "Content and target_language are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Call AI provider directly
        provider = AIProviderFactory.get_provider()
        translated_data = provider.translate_article(content, target_language)
        
        AIGeneration.objects.create(
            stage="translate", 
            language=target_language, 
            input_payload=payload, 
            output_payload=translated_data, 
            sources=[], 
            quality_score=0.85
        )
        
        return ok({"translation": translated_data})
        
    except Exception as e:
        return Response(
            {"error": f"Failed to translate article: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Admin AI Generation Flow Endpoints
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_ai_generate_outline(request):
    """
    Admin endpoint: Generate outline for blog post creation
    POST /api/v1/ai/generate/outline
    """
    try:
        payload = request.data
        topic = payload.get("topic", "").strip()
        target_audience = payload.get("target_audience", "EU business owners")
        
        if not topic:
            return Response(
                {"error": "Topic is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate outline using AI provider
        provider = AIProviderFactory.get_provider()
        outline_data = provider.generate_outline(topic, target_audience)
        
        # Log AI generation
        log = AIGeneration.objects.create(
            stage="outline", 
            language=payload.get("language", "en"), 
            input_payload=payload, 
            output_payload=outline_data,
            sources=[s.get("url", "") for s in outline_data.get("sources", [])], 
            quality_score=0.85
        )
        
        return Response({
            "outline": outline_data,
            "generation_id": str(log.id),
            "next_step": "/api/v1/ai/generate/draft"
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"error": f"Failed to generate outline: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_ai_generate_draft(request):
    """
    Admin endpoint: Generate draft from outline
    POST /api/v1/ai/generate/draft
    """
    try:
        payload = request.data
        outline = payload.get("outline", "")
        word_count = payload.get("word_count", 800)
        
        if not outline:
            return Response(
                {"error": "Outline is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate draft using AI provider
        provider = AIProviderFactory.get_provider()
        if isinstance(outline, dict):
            outline = json.dumps(outline)
        
        draft_data = provider.generate_draft(outline, word_count)
        
        # Log AI generation
        log = AIGeneration.objects.create(
            stage="draft", 
            language=payload.get("language", "en"), 
            input_payload=payload, 
            output_payload=draft_data,
            sources=[c.get("url", "") for c in draft_data.get("citations", [])], 
            quality_score=0.88
        )
        
        return Response({
            "draft": draft_data,
            "generation_id": str(log.id),
            "next_step": "/api/v1/ai/generate/seo"
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"error": f"Failed to generate draft: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_ai_generate_seo(request):
    """
    Admin endpoint: Generate SEO metadata from content
    POST /api/v1/ai/generate/seo
    """
    try:
        payload = request.data
        title = payload.get("title", "")
        content = payload.get("content", "")
        target_keywords = payload.get("target_keywords", "")
        
        if not content:
            return Response(
                {"error": "Content is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate SEO using AI provider
        provider = AIProviderFactory.get_provider()
        
        # Combine title and content for SEO analysis
        full_content = f"# {title}\n\n{content}" if title else content
        keywords_list = target_keywords.split(',') if isinstance(target_keywords, str) else []
        
        seo_data = provider.generate_seo(full_content, keywords_list)
        
        # Log AI generation
        AIGeneration.objects.create(
            stage="seo", 
            language=payload.get("language", "en"), 
            input_payload=payload, 
            output_payload=seo_data,
            sources=[], 
            quality_score=0.9
        )
        
        return Response({
            "seo": seo_data,
            "next_step": "/api/v1/posts"
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"error": f"Failed to generate SEO: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_create_post_from_ai(request):
    """
    Admin endpoint: Create blog post from AI-generated content
    POST /api/v1/posts
    """
    try:
        payload = request.data
        
        # Extract required data
        title = payload.get("title", "")
        content = payload.get("content", "")
        excerpt = payload.get("excerpt", "")
        seo_data = payload.get("seo", {})
        category_id = payload.get("category_id")
        
        if not title or not content:
            return Response(
                {"error": "Title and content are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create blog post with status='review' (between draft and published)
        from django.utils.text import slugify
        
        # Get category if provided
        category = None
        if category_id:
            try:
                category = BlogCategory.objects.get(id=category_id)
            except BlogCategory.DoesNotExist:
                pass
        
        # Generate slug from title
        slug = slugify(title)
        if BlogPost.objects.filter(slug=slug).exists():
            slug = f"{slug}-{int(timezone.now().timestamp())}"
        
        # Create the blog post
        post = BlogPost.objects.create(
            title_en=title,
            slug=slug,
            excerpt_en=excerpt or title[:200],
            content_en=content,
            author=request.user,
            category=category,
            status='review',  # Special status for AI-generated content awaiting review
            
            # SEO fields from AI generation (using SEOMixin fields)
            meta_title=seo_data.get('meta_title', title)[:70],
            meta_description=seo_data.get('meta_desc', excerpt)[:160],
        )
        
        return Response({
            "post_id": post.id,
            "status": post.status,
            "title": post.title_en,
            "slug": post.slug,
            "next_step": f"/api/v1/posts/{post.id}/publish"
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {"error": f"Failed to create post: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_publish_post(request, post_id):
    """
    Admin endpoint: Publish a blog post after reliability checks
    POST /api/v1/posts/<id>/publish
    """
    try:
        # Get the post
        try:
            post = BlogPost.objects.get(id=post_id)
        except BlogPost.DoesNotExist:
            return Response(
                {"error": "Post not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Reliability gates - check for content quality
        canonical_lang = "en"  # Default to English for now
        content_html = post.get_content(canonical_lang)
        
        # Check 1: Verify citations exist if content has monetary/date claims
        if _has_claims_needing_citation(content_html):
            # For current model structure, check if content has citation markers
            has_citations = "[1]" in content_html or "[2]" in content_html or "http" in content_html
            
            if not has_citations:
                return Response(
                    {"error": "Citations required for monetary/date claims"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Check 2: Verify internal links (basic check for now)
        internal_link_patterns = ["/how-it-works", "/countries", "/categories"]
        internal_link_count = sum(1 for pattern in internal_link_patterns if pattern in content_html)
        
        if internal_link_count < 2:
            return Response(
                {"error": f"At least 2 internal links required, found {internal_link_count}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # All checks passed - publish the post
        post.status = 'published'
        post.published_at = timezone.now()
        post.save()
        
        return Response({
            "message": "Post published successfully",
            "post_id": post.id,
            "status": post.status,
            "published_at": post.published_at,
            "url": f"/blog/{post.slug}"
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"error": f"Failed to publish post: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )