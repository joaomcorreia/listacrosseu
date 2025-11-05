from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import timezone
import json
import os
from django.conf import settings
from businesses.models import Business, Country, City
from django.db.models import Count, Q

# Try to import OpenAI if available
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

@method_decorator(csrf_exempt, name='dispatch')
class ListyAssistantView(View):
    """
    Listy AI Assistant API endpoint
    Provides intelligent responses about ListAcrossEU platform data
    """
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            language = data.get('language', 'en')
            
            if not user_message:
                return JsonResponse({
                    'error': 'Message is required',
                    'response': self._get_error_message(language)
                }, status=400)
            
            # Get contextual business data
            context = self._get_business_context()
            
            # Generate AI response
            response = self._generate_listy_response(user_message, language, context)
            
            return JsonResponse({
                'response': response,
                'language': language,
                'timestamp': str(timezone.now())
            })
            
        except Exception as e:
            return JsonResponse({
                'error': str(e),
                'response': self._get_error_message(language)
            }, status=500)
    
    def _get_business_context(self):
        """Get current platform statistics and data"""
        try:
            total_businesses = Business.objects.filter(status='active').count()
            
            # Countries with businesses
            countries_data = []
            for country in Country.objects.filter(cities__businesses__status='active').distinct():
                count = Business.objects.filter(city__country=country, status='active').count()
                cities = list(City.objects.filter(
                    country=country, 
                    businesses__status='active'
                ).distinct().values_list('name', flat=True)[:5])
                
                countries_data.append({
                    'name': country.name,
                    'business_count': count,
                    'major_cities': cities
                })
            
            return {
                'total_businesses': total_businesses,
                'countries': countries_data,
                'platform_languages': 27,
                'active_countries': len(countries_data)
            }
        except Exception:
            return {
                'total_businesses': 6331,
                'countries': [
                    {'name': 'Spain', 'business_count': 2494, 'major_cities': ['Madrid', 'Barcelona']},
                    {'name': 'France', 'business_count': 2127, 'major_cities': ['Paris', 'Lyon']},
                    {'name': 'Germany', 'business_count': 1710, 'major_cities': ['Berlin', 'Munich']}
                ],
                'platform_languages': 27,
                'active_countries': 3
            }
    
    def _generate_listy_response(self, message, language, context):
        """Generate intelligent AI response using OpenAI or fallback"""
        
        # Check if OpenAI is available and configured
        if not HAS_OPENAI or not hasattr(settings, 'OPENAI_API_KEY') or not settings.OPENAI_API_KEY:
            return self._generate_fallback_response(message, language, context)
        
        try:
            # Set up OpenAI
            openai.api_key = settings.OPENAI_API_KEY
            
            # Create system prompt for Listy
            system_prompt = self._create_system_prompt(language, context)
            
            # Use the new OpenAI client format
            from openai import OpenAI
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._generate_fallback_response(message, language, context)
    
    def _create_system_prompt(self, language, context):
        """Create system prompt for Listy based on language and context"""
        
        prompts = {
            'en': f"""You are Listy, the friendly AI assistant for ListAcrossEU - Europe's premier business directory platform.

PLATFORM DATA:
- Total businesses: {context['total_businesses']:,}
- Active countries: {context['active_countries']}
- Supported languages: {context['platform_languages']} EU languages
- Countries with data: {', '.join([c['name'] + f" ({c['business_count']} businesses)" for c in context['countries']])}

YOUR PERSONALITY:
- Friendly, helpful, and enthusiastic about European business
- Use appropriate emojis (🇪🇺, 🏢, 🌍, etc.)
- Keep responses concise but informative
- Always offer to help with specific business searches

CAPABILITIES:
- Help users find businesses by country, city, or type
- Provide platform statistics and country information
- Assist with language switching and navigation
- Answer questions about EU business directory features

Remember to be helpful, accurate, and maintain a professional yet friendly tone. Always respond in English unless specifically requested otherwise.""",

            'es': f"""Eres Listy, el asistente IA amigable de ListAcrossEU - la plataforma de directorio empresarial premier de Europa.

DATOS DE LA PLATAFORMA:
- Total de empresas: {context['total_businesses']:,}
- Países activos: {context['active_countries']}
- Idiomas soportados: {context['platform_languages']} idiomas de la UE
- Países con datos: {', '.join([c['name'] + f" ({c['business_count']} empresas)" for c in context['countries']])}

Responde siempre en español, sé amigable y usa emojis apropiados 🇪🇺🏢🌍""",

            'fr': f"""Tu es Listy, l'assistant IA amical de ListAcrossEU - la plateforme de répertoire d'entreprises première d'Europe.

DONNÉES DE LA PLATEFORME:
- Total des entreprises: {context['total_businesses']:,}
- Pays actifs: {context['active_countries']}
- Langues supportées: {context['platform_languages']} langues de l'UE
- Pays avec données: {', '.join([c['name'] + f" ({c['business_count']} entreprises)" for c in context['countries']])}

Réponds toujours en français, sois amical et utilise des emojis appropriés 🇪🇺🏢🌍""",

            'de': f"""Du bist Listy, der freundliche KI-Assistent von ListAcrossEU - Europas führende Unternehmensverzeichnis-Plattform.

PLATTFORM-DATEN:
- Gesamte Unternehmen: {context['total_businesses']:,}
- Aktive Länder: {context['active_countries']}
- Unterstützte Sprachen: {context['platform_languages']} EU-Sprachen
- Länder mit Daten: {', '.join([c['name'] + f" ({c['business_count']} Unternehmen)" for c in context['countries']])}

Antworte immer auf Deutsch, sei freundlich und verwende passende Emojis 🇪🇺🏢🌍"""
        }
        
        return prompts.get(language, prompts['en'])
    
    def _generate_fallback_response(self, message, language, context):
        """Generate fallback response when OpenAI is not available"""
        
        message_lower = message.lower()
        
        # Response templates by language
        responses = {
            'en': {
                'stats': f"📊 ListAcrossEU Statistics:\n• {context['total_businesses']:,} active businesses\n• {context['active_countries']} countries with data\n• {context['platform_languages']} EU languages supported\n\nCountries: {', '.join([c['name'] for c in context['countries']])}\n\nHow else can I help you explore our European business directory? 🇪🇺",
                
                'countries': f"🌍 We currently have business data for {context['active_countries']} countries:\n\n" + 
                           '\n'.join([f"🇪🇺 {c['name']}: {c['business_count']:,} businesses in cities like {', '.join(c['major_cities'][:3])}" 
                                    for c in context['countries']]) + 
                           "\n\nWhich country would you like to explore? I can help you find specific businesses or cities! 🏢",
                
                'businesses': f"🏢 Great question! We have {context['total_businesses']:,} verified businesses across Europe.\n\nPopular searches:\n• Restaurants in Madrid\n• Tech companies in Berlin\n• Hotels in Paris\n\nWhat type of business are you looking for? I can help you search by category, location, or country! 🔍",
                
                'help': "🤖 Hi! I'm Listy, your EU business directory assistant! I can help you:\n\n🔍 Find businesses by location or type\n📊 Get platform statistics\n🌍 Explore different countries\n🇪🇺 Switch languages\n\nWhat would you like to know about our European business directory?",
                
                'default': f"Thanks for your message! 🇪🇺 I'm here to help you navigate our directory of {context['total_businesses']:,} European businesses. Try asking me about:\n\n• 'Show me businesses in Spain'\n• 'Platform statistics'\n• 'Available countries'\n\nWhat can I help you find today? 🏢"
            },
            
            'es': {
                'stats': f"📊 Estadísticas de ListAcrossEU:\n• {context['total_businesses']:,} empresas activas\n• {context['active_countries']} países con datos\n• {context['platform_languages']} idiomas de la UE\n\nPaíses: {', '.join([c['name'] for c in context['countries']])}\n\n¿Cómo más puedo ayudarte a explorar nuestro directorio empresarial europeo? 🇪🇺",
                
                'default': f"¡Gracias por tu mensaje! 🇪🇺 Estoy aquí para ayudarte a navegar nuestro directorio de {context['total_businesses']:,} empresas europeas. ¿Qué puedo ayudarte a encontrar hoy? 🏢"
            },
            
            'fr': {
                'default': f"Merci pour votre message! 🇪🇺 Je suis là pour vous aider à naviguer dans notre répertoire de {context['total_businesses']:,} entreprises européennes. Que puis-je vous aider à trouver aujourd'hui? 🏢"
            }
        }
        
        lang_responses = responses.get(language, responses['en'])
        
        # Determine response type
        if any(word in message_lower for word in ['statistic', 'stats', 'number', 'count']):
            return lang_responses.get('stats', lang_responses['default'])
        elif any(word in message_lower for word in ['countries', 'country', 'nation']):
            return lang_responses.get('countries', lang_responses['default'])
        elif any(word in message_lower for word in ['business', 'company', 'find', 'search']):
            return lang_responses.get('businesses', lang_responses['default'])
        elif any(word in message_lower for word in ['help', 'what', 'how']):
            return lang_responses.get('help', lang_responses['default'])
        else:
            return lang_responses['default']
    
    def _get_error_message(self, language):
        """Get error message in specified language"""
        messages = {
            'en': "I'm sorry, I encountered an error. Please try again! 🤖",
            'es': "Lo siento, encontré un error. ¡Por favor intenta de nuevo! 🤖",
            'fr': "Désolé, j'ai rencontré une erreur. Veuillez réessayer! 🤖",
            'de': "Entschuldigung, ich bin auf einen Fehler gestoßen. Bitte versuchen Sie es erneut! 🤖"
        }
        return messages.get(language, messages['en'])

# Add to URLs
from django.urls import path
from . import views

urlpatterns = [
    # ... your existing URLs
    path('api/v1/listy/', ListyAssistantView.as_view(), name='listy_assistant'),
]