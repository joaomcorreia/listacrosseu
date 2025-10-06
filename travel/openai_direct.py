"""
Direct OpenAI Integration for Travel Content Generation
Fallback when MagicAI API is not available
"""
from openai import OpenAI
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class DirectOpenAIClient:
    """
    Direct OpenAI client for travel content generation
    """
    
    def __init__(self):
        self.api_key = getattr(settings, 'OPENAI_API_KEY', '')
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    def generate_city_guide(self, city_name: str, country: str, language: str = 'en') -> dict:
        """Generate city guide using OpenAI directly"""
        
        prompt = f"""
        Write a comprehensive travel guide for {city_name}, {country} in {language}.
        
        Include:
        1. Introduction and overview
        2. Top 10 must-see attractions with descriptions
        3. Best restaurants and local cuisine recommendations
        4. Transportation tips and getting around
        5. Where to stay (different budget levels)
        6. Local culture and customs
        7. Best time to visit and weather
        8. Safety tips for travelers
        9. Hidden gems and local secrets
        10. Day-by-day itinerary suggestions
        
        Make it engaging, informative, and SEO-optimized.
        Target length: 2000-3000 words.
        Use markdown formatting with headers and lists.
        """
        
        if not self.client:
            return {
                'success': False,
                'error': 'OpenAI API key not configured'
            }
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Use cheaper model for testing
                messages=[
                    {"role": "system", "content": "You are an expert travel writer who creates comprehensive, engaging city guides."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=3000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            return {
                'success': True,
                'content': content,
                'title': f"Complete {city_name} Travel Guide 2025",
                'model_used': 'openai-direct'
            }
            
        except Exception as e:
            logger.error(f"OpenAI direct error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_restaurant_review(self, restaurant_name: str, city: str, cuisine_type: str) -> dict:
        """Generate restaurant review using OpenAI"""
        
        prompt = f"""
        Write a detailed restaurant review for {restaurant_name} in {city}.
        
        Cuisine type: {cuisine_type}
        
        Include:
        - Atmosphere and ambiance description
        - Menu highlights and must-try dishes
        - Price range and value for money
        - Service quality and staff
        - Best dishes to order
        - Reservation and visiting tips
        - Overall rating and recommendation
        
        Write in an engaging, food blogger style.
        Make it feel authentic and helpful for travelers.
        """
        
        if not self.client:
            return {
                'success': False,
                'error': 'OpenAI API key not configured'
            }
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional food critic and travel blogger."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.8
            )
            
            content = response.choices[0].message.content
            
            return {
                'success': True,
                'content': content,
                'title': f"{restaurant_name} Review - {city} Dining Experience"
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Add OpenAI settings to your .env file
OPENAI_INTEGRATION_SETTINGS = """
# Add these to your .env file:
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_ENABLED=True
"""