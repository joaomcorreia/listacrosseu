import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from .ai_providers import AIProviderFactory


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_outline(request):
    """
    Generate blog post outline via AI
    Expected payload: {"topic": "string", "target_audience": "string"}
    """
    try:
        data = request.data
        topic = data.get('topic', '').strip()
        target_audience = data.get('target_audience', '').strip()
        
        if not topic:
            return Response(
                {"error": "Topic is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get AI provider
        provider = AIProviderFactory.get_provider()
        
        # Generate outline
        outline = provider.generate_outline(topic, target_audience or "general business audience")
        
        return Response(outline, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"error": f"Failed to generate outline: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_draft(request):
    """
    Generate blog post draft from outline
    Expected payload: {"outline": "string", "word_count": 800}
    """
    try:
        data = request.data
        outline = data.get('outline', '').strip()
        word_count = data.get('word_count', 800)
        
        if not outline:
            return Response(
                {"error": "Outline is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get AI provider
        provider = AIProviderFactory.get_provider()
        
        # Generate draft
        draft = provider.generate_draft(outline, word_count)
        
        return Response(draft, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"error": f"Failed to generate draft: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_seo(request):
    """
    Generate SEO meta data for blog post
    Expected payload: {"content": "string", "target_keywords": ["keyword1", "keyword2"]}
    """
    try:
        data = request.data
        content = data.get('content', '').strip()
        target_keywords = data.get('target_keywords', [])
        
        if not content:
            return Response(
                {"error": "Content is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get AI provider
        provider = AIProviderFactory.get_provider()
        
        # Generate SEO
        seo_data = provider.generate_seo(content, target_keywords)
        
        return Response(seo_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"error": f"Failed to generate SEO: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def translate_article(request):
    """
    Translate blog post content to target language
    Expected payload: {"content": "string", "target_language": "fr"}
    """
    try:
        data = request.data
        content = data.get('content', '').strip()
        target_language = data.get('target_language', '').strip().lower()
        
        if not content or not target_language:
            return Response(
                {"error": "Content and target_language are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate target language
        valid_languages = ['fr', 'nl', 'pt', 'de', 'es', 'ar']
        if target_language not in valid_languages:
            return Response(
                {"error": f"Target language must be one of: {', '.join(valid_languages)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get AI provider
        provider = AIProviderFactory.get_provider()
        
        # Translate content
        translated = provider.translate_article(content, target_language)
        
        return Response(translated, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"error": f"Failed to translate article: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([])  # Allow unauthenticated access for status check
def ai_status(request):
    """
    Check AI provider status and configuration
    """
    try:
        provider_name = getattr(settings, 'AI_PROVIDER', 'mock')
        provider = AIProviderFactory.get_provider()
        
        return Response({
            "status": "operational",
            "provider": provider_name,
            "provider_class": provider.__class__.__name__,
            "available_functions": [
                "generate_outline",
                "generate_draft", 
                "generate_seo",
                "translate_article"
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"error": f"AI service unavailable: {str(e)}"}, 
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
