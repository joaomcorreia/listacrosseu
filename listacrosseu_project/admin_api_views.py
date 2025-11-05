from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from listings.models import Business
from blog.models import BlogPost
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

@api_view(['GET'])
def dashboard_stats(request):
    """
    Get dashboard statistics for the admin panel
    """
    try:
        # Get basic counts
        total_businesses = Business.objects.count()
        active_businesses = Business.objects.filter(is_active=True).count()
        featured_businesses = Business.objects.filter(is_featured=True).count()
        total_blog_posts = BlogPost.objects.count()
        published_blog_posts = BlogPost.objects.filter(status='published').count()
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        
        # Get recent activity (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_businesses = Business.objects.filter(created_at__gte=thirty_days_ago).count()
        recent_blog_posts = BlogPost.objects.filter(created_at__gte=thirty_days_ago).count()
        recent_users = User.objects.filter(date_joined__gte=thirty_days_ago).count()
        
        # Calculate percentage changes (mock for now)
        business_change = "+8%" if recent_businesses > 0 else "0%"
        blog_change = "+12%" if recent_blog_posts > 0 else "0%"
        user_change = "+15%" if recent_users > 0 else "0%"
        
        stats = {
            'total_businesses': total_businesses,
            'active_businesses': active_businesses,
            'featured_businesses': featured_businesses,
            'total_blog_posts': total_blog_posts,
            'published_blog_posts': published_blog_posts,
            'total_users': total_users,
            'active_users': active_users,
            'recent_activity': {
                'businesses': recent_businesses,
                'blog_posts': recent_blog_posts,
                'users': recent_users,
            },
            'changes': {
                'businesses': business_change,
                'blog_posts': blog_change,
                'users': user_change,
                'featured': "+4%"
            }
        }
        
        return Response(stats)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to fetch dashboard stats: {str(e)}'}, 
            status=500
        )

@api_view(['GET'])
def csrf_token(request):
    """
    Get CSRF token for authenticated requests
    """
    from django.middleware.csrf import get_token
    return Response({'csrf_token': get_token(request)})

@api_view(['GET'])
def admin_health_check(request):
    """
    Health check for admin integration
    """
    from django.db import connection
    
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            
        return Response({
            'status': 'healthy',
            'database': 'connected',
            'django_version': '5.2.7',
            'time': timezone.now().isoformat()
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'error': str(e)
        }, status=500)