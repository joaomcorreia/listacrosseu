from django.utils.deprecation import MiddlewareMixin
from django.http import Http404
from .models import Website


class SubdomainMiddleware(MiddlewareMixin):
    """Middleware to handle subdomain routing for user websites"""
    
    def process_request(self, request):
        """Process incoming requests and route subdomains to user websites"""
        
        host = request.get_host().lower()
        
        # Skip if not a listacrosseu.com domain
        if not host.endswith('.listacrosseu.com') or host == 'listacrosseu.com':
            return None
        
        # Extract subdomain
        subdomain = host.split('.')[0]
        
        # Skip admin and api subdomains
        if subdomain in ['admin', 'api', 'www', 'mail', 'ftp']:
            return None
        
        try:
            # Find the website with this domain
            domain_name = host
            website = Website.objects.select_related('domain', 'user').get(
                domain__domain_name=domain_name,
                status='published'
            )
            
            # Add website to request
            request.website = website
            request.is_user_website = True
            
        except Website.DoesNotExist:
            # If no website found, raise 404
            raise Http404("Website not found")
        
        return None