from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.translation import activate, gettext as _
from accounts.models import UserProfile


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assistant_chat(request):
    """
    Assistant endpoint that responds in user's preferred language
    """
    user_message = request.data.get('message', '')
    
    # Get user's language preference
    try:
        profile = UserProfile.objects.get(user=request.user)
        user_language = profile.get_effective_language()
        
        # Check context (dashboard vs website)
        context = request.data.get('context', 'website')
        if context == 'dashboard' and profile.arabic_on_dashboard:
            user_language = 'ar'
        elif context == 'website' and profile.arabic_on_website:
            user_language = 'ar'
            
    except UserProfile.DoesNotExist:
        user_language = 'en'
    
    # Activate the user's language
    activate(user_language)
    
    # Generate response based on language
    response_text = generate_assistant_response(user_message, user_language)
    
    return Response({
        'message': response_text,
        'language': user_language,
        'context': request.data.get('context', 'website'),
        'user': request.user.username
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def assistant_test(request):
    """
    Test endpoint to verify language switching works correctly
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
        effective_language = profile.get_effective_language()
        
        # Activate the language and get translated messages
        activate(effective_language)
        
        test_messages = {
            'welcome': _('Welcome to ListAcross EU'),
            'help': _('How can I help you today?'),
            'language_active': _('Language is now active'),
            'arabic_dashboard': profile.arabic_on_dashboard,
            'arabic_website': profile.arabic_on_website,
            'preferred_language': profile.preferred_language,
        }
        
    except UserProfile.DoesNotExist:
        activate('en')
        test_messages = {
            'welcome': _('Welcome to ListAcross EU'),
            'help': _('How can I help you today?'),
            'language_active': _('Language is now active'),
            'note': 'No user profile found, using default language'
        }
    
    return Response({
        'test_messages': test_messages,
        'current_language': effective_language if 'effective_language' in locals() else 'en',
        'user': request.user.username
    })


def generate_assistant_response(message, language):
    """
    Generate assistant response in the specified language
    """
    # Activate the language for proper translation
    activate(language)
    
    # Simple response logic - in a real application, this would be more sophisticated
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'bonjour', 'hola', 'merhaba', 'سلام', 'olá']):
        return _('Hello! How can I assist you with finding businesses in Europe today?')
    
    elif any(word in message_lower for word in ['help', 'aide', 'ayuda', 'ajuda', 'hilfe', 'مساعدة']):
        return _('I can help you find businesses, search by category, or provide information about our services. What would you like to know?')
    
    elif any(word in message_lower for word in ['business', 'company', 'entreprise', 'empresa', 'unternehmen', 'شركة']):
        return _('I can help you search for businesses by location, category, or name. You can also filter by verified businesses or featured listings.')
    
    elif any(word in message_lower for word in ['language', 'langue', 'idioma', 'sprache', 'لغة']):
        return _('Our platform supports multiple languages including English, French, Dutch, Portuguese, German, Spanish, and Arabic. You can change your language preferences in your profile settings.')
    
    else:
        return _('Thank you for your message. I\'m here to help you navigate ListAcross EU and find the best businesses across Europe. Could you please be more specific about what you\'re looking for?')


@api_view(['GET'])
def assistant_languages(request):
    """
    Get available languages for the assistant
    """
    languages = [
        {'code': 'en', 'name': 'English', 'native_name': 'English'},
        {'code': 'fr', 'name': 'French', 'native_name': 'Français'},
        {'code': 'nl', 'name': 'Dutch', 'native_name': 'Nederlands'},
        {'code': 'pt', 'name': 'Portuguese', 'native_name': 'Português'},
        {'code': 'de', 'name': 'German', 'native_name': 'Deutsch'},
        {'code': 'es', 'name': 'Spanish', 'native_name': 'Español'},
        {'code': 'ar', 'name': 'Arabic', 'native_name': 'العربية', 'rtl': True},
    ]
    
    return Response({'languages': languages})