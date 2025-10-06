"""
MagicAI Integration for Travel Content Generation
Connects Django Travel CMS with MagicAI API at tools.justcodeworks.net
"""
import requests
import json
from django.conf import settings
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class MagicAIClient:
    """
    Client for integrating with MagicAI API
    Generates travel content automatically
    """
    
    def __init__(self):
        self.base_url = getattr(settings, 'MAGICAI_BASE_URL', 'https://tools.justcodeworks.net')
        self.api_key = getattr(settings, 'MAGICAI_API_KEY', '')
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def generate_city_guide(self, city_name: str, country: str, language: str = 'en') -> Dict:
        """
        Generate a comprehensive city guide using MagicAI
        """
        prompt = f"""
        Write a comprehensive travel guide for {city_name}, {country} in {language}.
        
        Include:
        1. Introduction and overview
        2. Top 10 must-see attractions
        3. Best restaurants and local cuisine
        4. Transportation tips
        5. Where to stay (different budget levels)
        6. Local culture and customs
        7. Best time to visit
        8. Safety tips for travelers
        9. Hidden gems and local secrets
        10. Day-by-day itinerary suggestions
        
        Make it engaging, informative, and SEO-optimized.
        Target length: 2000-3000 words.
        """
        
        return self._generate_content(
            template='article-generator',
            prompt=prompt,
            title=f"Complete {city_name} Travel Guide 2025",
            language=language,
            ai_model='openai'  # Best for comprehensive travel guides
        )
    
    def generate_restaurant_review(self, restaurant_name: str, city: str, cuisine_type: str) -> Dict:
        """
        Generate restaurant review content
        """
        prompt = f"""
        Write a detailed restaurant review for {restaurant_name} in {city}.
        
        Cuisine type: {cuisine_type}
        
        Include:
        - Atmosphere and ambiance
        - Menu highlights and recommendations
        - Price range and value for money
        - Service quality
        - Best dishes to try
        - Reservation tips
        - Overall rating and recommendation
        
        Write in an engaging, food blogger style.
        """
        
        return self._generate_content(
            template='blog-post',
            prompt=prompt,
            title=f"{restaurant_name} Review - {city} Dining Experience",
            ai_model='gemini'  # Great for creative food and dining content
        )
    
    def generate_attraction_content(self, attraction_name: str, city: str, attraction_type: str) -> Dict:
        """
        Generate content about tourist attractions
        """
        prompt = f"""
        Write engaging content about {attraction_name} in {city}.
        
        Attraction type: {attraction_type}
        
        Include:
        - Historical background and significance
        - What to expect when visiting
        - Best times to visit (season, time of day)
        - Ticket prices and booking information
        - How to get there (transportation)
        - Photography tips
        - Nearby attractions to combine in a visit
        - Insider tips from locals
        
        Make it informative yet exciting to inspire travel.
        """
        
        return self._generate_content(
            template='article-generator',
            prompt=prompt,
            title=f"Visiting {attraction_name}: Complete Guide for {city} Travelers",
            ai_model='anthropic'  # Excellent for detailed, thoughtful content
        )
    
    def generate_travel_itinerary(self, destination: str, duration_days: int, travel_style: str = 'balanced') -> Dict:
        """
        Generate day-by-day travel itinerary
        """
        prompt = f"""
        Create a detailed {duration_days}-day travel itinerary for {destination}.
        
        Travel style: {travel_style} (budget-conscious, luxury, adventure, cultural, family-friendly)
        
        For each day include:
        - Morning activities (9 AM - 12 PM)
        - Afternoon activities (12 PM - 5 PM)  
        - Evening activities (5 PM - 9 PM)
        - Recommended restaurants for meals
        - Transportation between locations
        - Approximate costs
        - Alternative options for bad weather
        
        Make it practical and actionable with specific times and locations.
        """
        
        return self._generate_content(
            template='article-generator',
            prompt=prompt,
            title=f"Perfect {duration_days}-Day {destination} Itinerary",
            ai_model='openai'  # Best for structured planning and itineraries
        )
    
    def generate_business_description(self, business_name: str, business_type: str, city: str) -> Dict:
        """
        Generate business descriptions for directory listings
        """
        prompt = f"""
        Write a compelling business description for {business_name}, a {business_type} in {city}.
        
        Include:
        - What makes this business special
        - Key services or products offered
        - Target audience
        - Unique selling points
        - Why travelers should visit
        
        Keep it concise but engaging (150-300 words).
        Make it SEO-friendly and conversion-focused.
        """
        
        return self._generate_content(
            template='product-description',
            prompt=prompt,
            title=f"{business_name} - {business_type} in {city}",
            ai_model='gemini'  # Great for marketing and business descriptions
        )
    
    def _generate_content(self, template: str, prompt: str, title: str = "", language: str = 'en', ai_model: str = 'openai') -> Dict:
        """
        Internal method to call MagicAI API with multiple AI provider support
        """
        try:
            payload = {
                'template': template,
                'prompt': prompt,
                'title': title,
                'language': language,
                'ai_model': ai_model,  # openai, gemini, anthropic, etc.
                'creativity': 0.7,  # Balance between creative and factual
                'max_tokens': 3000
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'content': response.json().get('content', ''),
                    'title': title,
                    'tokens_used': response.json().get('tokens_used', 0),
                    'model_used': ai_model
                }
            else:
                logger.error(f"MagicAI API error: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'error': f"API error: {response.status_code}"
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"MagicAI connection error: {str(e)}")
            return {
                'success': False,
                'error': f"Connection error: {str(e)}"
            }
    
    def generate_travel_image(self, description: str, style: str = 'realistic') -> Dict:
        """
        Generate travel destination images using StableDiffusion
        """
        try:
            payload = {
                'prompt': f"Beautiful travel destination: {description}, {style} photography style, high quality, scenic view",
                'style': style,
                'size': '1024x1024',
                'steps': 20
            }
            
            response = requests.post(
                f"{self.base_url}/api/image/generate",
                headers=self.headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'image_url': response.json().get('image_url', ''),
                    'description': description
                }
            else:
                return {
                    'success': False,
                    'error': f"Image generation failed: {response.status_code}"
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"Image generation error: {str(e)}"
            }
    
    def generate_audio_guide(self, text_content: str, voice_type: str = 'professional') -> Dict:
        """
        Generate audio travel guides using TTS
        """
        try:
            payload = {
                'text': text_content,
                'voice': voice_type,
                'language': 'en',
                'speed': 1.0
            }
            
            response = requests.post(
                f"{self.base_url}/api/tts/generate",
                headers=self.headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'audio_url': response.json().get('audio_url', ''),
                    'duration': response.json().get('duration', 0)
                }
            else:
                return {
                    'success': False,
                    'error': f"TTS generation failed: {response.status_code}"
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"TTS error: {str(e)}"
            }
    
    def generate_seo_meta(self, content: str, target_keywords: List[str] = None) -> Dict:
        """
        Generate SEO meta description and keywords from content
        """
        keywords = ", ".join(target_keywords) if target_keywords else ""
        
        prompt = f"""
        Based on this travel content, generate SEO metadata:
        
        Content: {content[:500]}...
        Target keywords: {keywords}
        
        Generate:
        1. Meta title (50-60 characters)
        2. Meta description (150-160 characters)  
        3. Focus keyphrase
        4. Additional relevant keywords (comma-separated)
        
        Make it optimized for travel searches and Google rankings.
        """
        
        return self._generate_content(
            template='seo-meta',
            prompt=prompt,
            title="SEO Metadata Generation"
        )

# Convenience functions for Django models
def auto_generate_article_content(city, category_name="City Guides"):
    """
    Auto-generate article content for a city using MagicAI
    """
    client = MagicAIClient()
    result = client.generate_city_guide(
        city_name=city.name,
        country=city.country.name if city.country else "Europe"
    )
    
    if result.get('success'):
        return {
            'title': result.get('title', f"{city.name} Travel Guide"),
            'content': result.get('content', ''),
            'excerpt': result.get('content', '')[:200] + '...',
            'seo_title': result.get('title', ''),
            'meta_description': result.get('content', '')[:160] + '...'
        }
    
    return None

def auto_generate_business_content(business):
    """
    Auto-generate business descriptions using MagicAI
    """
    client = MagicAIClient()
    result = client.generate_business_description(
        business_name=business.name,
        business_type=business.category.name if business.category else "Business",
        city=business.city.name if business.city else "Europe"
    )
    
    if result.get('success'):
        return result.get('content', '')
    
    return None

def create_complete_travel_package(city_name: str, country: str = "Europe"):
    """
    Create a complete travel content package using multiple MagicAI APIs
    Includes: article, images, and audio guide
    """
    client = MagicAIClient()
    
    # Generate comprehensive article content
    article_result = client.generate_city_guide(city_name, country)
    
    # Generate destination image
    image_result = client.generate_travel_image(
        f"{city_name} city center, beautiful architecture, tourist destination",
        style="photographic"
    )
    
    # Create audio guide from article content
    audio_result = None
    if article_result.get('success'):
        # Create shorter version for audio
        audio_text = article_result.get('content', '')[:1000] + "..."
        audio_result = client.generate_audio_guide(audio_text, voice_type='professional')
    
    return {
        'article': article_result,
        'image': image_result, 
        'audio': audio_result,
        'city': city_name,
        'country': country
    }