from django.utils import translation
from django.conf import settings
from accounts.models import UserProfile


class UserLanguageMiddleware:
    """
    Custom middleware to activate user's preferred language based on their profile settings
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get language from various sources
        language = self.get_user_language(request)
        
        if language:
            translation.activate(language)
            request.LANGUAGE_CODE = language
        
        response = self.get_response(request)
        
        # Deactivate to prevent thread-local issues
        translation.deactivate()
        
        return response
    
    def get_user_language(self, request):
        """
        Determine the user's preferred language from multiple sources:
        1. URL parameter (?lang=xx)
        2. User profile settings (if authenticated)
        3. Session language
        4. Cookie language
        5. Browser Accept-Language header
        6. Default language
        """
        
        # 1. Check URL parameter
        url_lang = request.GET.get('lang')
        if url_lang and url_lang in dict(settings.LANGUAGES):
            request.session['django_language'] = url_lang
            return url_lang
        
        # 2. Check user profile (if authenticated)
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                effective_lang = profile.get_effective_language()
                
                # Check if user has Arabic preferences
                if request.path.startswith('/dashboard/') and profile.arabic_on_dashboard:
                    return 'ar'
                elif not request.path.startswith('/dashboard/') and profile.arabic_on_website:
                    return 'ar'
                else:
                    return effective_lang
            except UserProfile.DoesNotExist:
                pass
        
        # 3. Check session
        session_lang = request.session.get('django_language')
        if session_lang and session_lang in dict(settings.LANGUAGES):
            return session_lang
        
        # 4. Check cookie
        cookie_lang = request.COOKIES.get('django_language')
        if cookie_lang and cookie_lang in dict(settings.LANGUAGES):
            return cookie_lang
        
        # 5. Check Accept-Language header
        from django.utils.translation import get_language_from_request
        browser_lang = get_language_from_request(request)
        if browser_lang:
            return browser_lang
        
        # 6. Return default
        return settings.LANGUAGE_CODE


class AssistantLanguageMiddleware:
    """
    Middleware to handle language preferences for assistant responses
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Set assistant language context
        if request.path.startswith('/api/assistant/') and request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                assistant_language = profile.get_effective_language()
                
                # Set in request context for assistant views
                request.assistant_language = assistant_language
                
            except UserProfile.DoesNotExist:
                request.assistant_language = settings.LANGUAGE_CODE
        
        response = self.get_response(request)
        return response