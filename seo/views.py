from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from django.conf import settings
from listings.models import Business


def sitemap(request):
    """Generate XML sitemap"""
    template = loader.get_template('seo/sitemap.xml')
    
    # Get all active businesses
    businesses = Business.objects.filter(is_active=True)
    
    context = {
        'businesses': businesses,
        'domain': request.get_host(),
        'protocol': 'https' if request.is_secure() else 'http',
    }
    
    xml_content = template.render(context)
    return HttpResponse(xml_content, content_type='application/xml')


def robots_txt(request):
    """Generate robots.txt"""
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        f"Sitemap: {request.build_absolute_uri('/seo/sitemap.xml')}",
    ]
    
    return HttpResponse("\n".join(lines), content_type="text/plain")