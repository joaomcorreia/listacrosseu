from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Article, ArticleView
import json


def hybrid_home(request):
    """Hybrid homepage showing both business directory and travel guides"""
    # Get featured articles for the homepage
    articles = Article.objects.filter(
        status='published'
    ).select_related('category', 'author').prefetch_related('tags').order_by(
        '-featured', '-published_at'
    )[:6]  # Limit to 6 for homepage display
    
    context = {
        'articles': articles,
        'page_title': 'ListAcross.eu - European Business Directory & Travel Guides',
        'meta_description': 'Discover businesses across the European Union and explore comprehensive travel guides for European destinations.'
    }
    
    return render(request, 'travel/hybrid_home.html', context)


def article_list(request):
    """Display list of published travel articles"""
    articles = Article.objects.filter(
        status='published'
    ).select_related('category', 'author').prefetch_related('tags').order_by(
        '-featured', '-published_at'
    )
    
    context = {
        'articles': articles,
        'page_title': 'European Travel Guides - ListAcross.eu',
        'meta_description': 'Discover Europe with AI-generated travel guides for major cities. Get comprehensive information about attractions, restaurants, and travel tips.'
    }
    
    return render(request, 'travel/article_list.html', context)


def article_detail(request, slug):
    """Display individual travel article"""
    article = get_object_or_404(
        Article.objects.select_related('category', 'author').prefetch_related('tags', 'cities'),
        slug=slug,
        status='published'
    )
    
    # Get related articles (same category, exclude current)
    related_articles = Article.objects.filter(
        category=article.category,
        status='published'
    ).exclude(id=article.id).order_by('-featured', '-published_at')[:4]
    
    context = {
        'article': article,
        'related_articles': related_articles,
        'page_title': article.title + ' - ListAcross.eu',
        'meta_description': article.meta_description or article.excerpt
    }
    
    return render(request, 'travel/article_detail.html', context)


@require_POST
@csrf_exempt
def track_view(request, article_id):
    """Track article view for analytics"""
    try:
        article = get_object_or_404(Article, id=article_id)
        
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Create view record
        ArticleView.objects.create(
            article=article,
            ip_address=ip,
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:200],
            referrer=request.META.get('HTTP_REFERER', '')[:200]
        )
        
        # Update article view count
        article.view_count += 1
        article.save(update_fields=['view_count'])
        
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def home_redirect(request):
    """Redirect home page to travel articles for now"""
    from django.shortcuts import redirect
    return redirect('travel:article_list')