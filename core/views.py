from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import SiteSettings

@require_http_methods(["GET", "POST"])
@staff_member_required
def site_settings(request):
    """
    API endpoint for site settings management
    """
    if request.method == "GET":
        try:
            settings = SiteSettings.get_settings()
            return JsonResponse({
                'ok': True,
                'settings': {
                    'siteName': settings.site_name,
                    'siteDescription': settings.site_description,
                    'contactEmail': settings.contact_email,
                    'supportEmail': settings.support_email,
                    'defaultLanguage': settings.default_language,
                    'enableRegistration': settings.enable_registration,
                    'enableComments': settings.enable_comments,
                    'maintenanceMode': settings.maintenance_mode,
                    'enableStarAnimation': settings.enable_star_animation,
                    'analyticsCode': settings.analytics_code,
                    'branding': {
                        'logo': settings.logo,
                        'favicon': settings.favicon,
                        'footerLogo': settings.footer_logo,
                    },
                    'socialLinks': {
                        'facebook': settings.facebook_url,
                        'twitter': settings.twitter_url,
                        'linkedin': settings.linkedin_url,
                        'instagram': settings.instagram_url,
                    },
                    'seoSettings': {
                        'defaultTitle': settings.default_title,
                        'defaultDescription': settings.default_description,
                        'defaultKeywords': settings.default_keywords,
                        'ogImageUrl': settings.og_image_url,
                    }
                }
            })
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=500)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            settings = SiteSettings.get_settings()
            
            # Update fields from request data
            if 'siteName' in data:
                settings.site_name = data['siteName']
            if 'siteDescription' in data:
                settings.site_description = data['siteDescription']
            if 'contactEmail' in data:
                settings.contact_email = data['contactEmail']
            if 'supportEmail' in data:
                settings.support_email = data['supportEmail']
            if 'defaultLanguage' in data:
                settings.default_language = data['defaultLanguage']
            if 'enableRegistration' in data:
                settings.enable_registration = data['enableRegistration']
            if 'enableComments' in data:
                settings.enable_comments = data['enableComments']
            if 'maintenanceMode' in data:
                settings.maintenance_mode = data['maintenanceMode']
            if 'enableStarAnimation' in data:
                settings.enable_star_animation = data['enableStarAnimation']
            if 'analyticsCode' in data:
                settings.analytics_code = data['analyticsCode']
            
            # Branding
            if 'branding' in data:
                branding = data['branding']
                if 'logo' in branding:
                    settings.logo = branding['logo']
                if 'favicon' in branding:
                    settings.favicon = branding['favicon']
                if 'footerLogo' in branding:
                    settings.footer_logo = branding['footerLogo']
            
            # Social links
            if 'socialLinks' in data:
                social = data['socialLinks']
                if 'facebook' in social:
                    settings.facebook_url = social['facebook']
                if 'twitter' in social:
                    settings.twitter_url = social['twitter']
                if 'linkedin' in social:
                    settings.linkedin_url = social['linkedin']
                if 'instagram' in social:
                    settings.instagram_url = social['instagram']
            
            # SEO settings
            if 'seoSettings' in data:
                seo = data['seoSettings']
                if 'defaultTitle' in seo:
                    settings.default_title = seo['defaultTitle']
                if 'defaultDescription' in seo:
                    settings.default_description = seo['defaultDescription']
                if 'defaultKeywords' in seo:
                    settings.default_keywords = seo['defaultKeywords']
                if 'ogImageUrl' in seo:
                    settings.og_image_url = seo['ogImageUrl']
            
            settings.save()
            
            return JsonResponse({'ok': True, 'message': 'Settings updated successfully'})
            
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=500)

def maintenance_status(request):
    """
    Public endpoint to check maintenance status
    """
    try:
        is_maintenance = SiteSettings.is_maintenance_mode()
        return JsonResponse({
            'maintenance_mode': is_maintenance,
            'status': 'maintenance' if is_maintenance else 'operational'
        })
    except Exception as e:
        return JsonResponse({
            'maintenance_mode': False,
            'status': 'operational',
            'error': 'Could not determine maintenance status'
        })

def animation_settings(request):
    """
    Public endpoint for animation settings
    """
    try:
        settings = SiteSettings.get_settings()
        return JsonResponse({
            'enableStarAnimation': settings.enable_star_animation,
        })
    except Exception as e:
        return JsonResponse({
            'enableStarAnimation': True,  # Default fallback
            'error': str(e)
        }, status=200)  # Still return 200 with default