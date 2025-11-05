import openai
import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import uuid
import os


class ImageGenerator:
    """Generate images using OpenAI DALL-E for travel content"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def generate_travel_image(self, destination, description, style="photorealistic"):
        """
        Generate a travel image for a destination
        
        Args:
            destination (str): City or location name
            description (str): Description of what to show
            style (str): Image style preference
            
        Returns:
            str: Path to saved image or None if failed
        """
        try:
            # Create a detailed prompt for travel images
            prompt = f"""
            A beautiful {style} photograph of {destination}, showing {description}.
            High quality, professional travel photography, vibrant colors, 
            capturing the essence of European travel and culture.
            No text or watermarks. Tourism promotional style.
            """
            
            # Generate image using DALL-E 3
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            # Get the image URL
            image_url = response.data[0].url
            
            # Download and save the image
            return self._download_and_save_image(image_url, destination)
            
        except Exception as e:
            print(f"Error generating image: {e}")
            return None
    
    def _download_and_save_image(self, image_url, destination):
        """Download image from URL and save to media storage"""
        try:
            # Generate unique filename
            filename = f"travel_images/{destination.lower().replace(' ', '_')}_{uuid.uuid4().hex[:8]}.png"
            
            # Download image
            response = requests.get(image_url)
            response.raise_for_status()
            
            # Save to Django media storage
            path = default_storage.save(filename, ContentFile(response.content))
            
            return path
            
        except Exception as e:
            print(f"Error saving image: {e}")
            return None
    
    def generate_article_images(self, article):
        """Generate multiple images for a travel article"""
        images = []
        
        # Main city image
        main_image = self.generate_travel_image(
            destination=article.title.replace("Travel Guide", "").replace("2025", "").strip(),
            description="iconic landmarks and cityscape",
            style="photorealistic"
        )
        if main_image:
            images.append({
                'path': main_image,
                'caption': f"Beautiful view of {article.title}",
                'type': 'hero'
            })
        
        # Additional themed images based on content
        themes = [
            ("historic architecture and monuments", "architectural"),
            ("local food and restaurants", "culinary"),
            ("parks and outdoor spaces", "nature"),
        ]
        
        destination = article.title.replace("Travel Guide", "").replace("2025", "").strip()
        
        for description, theme_type in themes:
            image_path = self.generate_travel_image(
                destination=destination,
                description=description,
                style="photorealistic"
            )
            if image_path:
                images.append({
                    'path': image_path,
                    'caption': f"{destination} - {description}",
                    'type': theme_type
                })
        
        return images


# Management command to generate images for existing articles
def generate_images_for_articles():
    """Generate images for all published articles without images"""
    from travel.models import Article, ArticleImage
    
    generator = ImageGenerator()
    articles_without_images = Article.objects.filter(
        status='published',
        images__isnull=True
    ).distinct()
    
    for article in articles_without_images:
        print(f"Generating images for: {article.title}")
        
        images = generator.generate_article_images(article)
        
        # Save images to the article
        for img_data in images:
            ArticleImage.objects.create(
                article=article,
                image=img_data['path'],
                caption=img_data['caption'],
                alt_text=img_data['caption'],
                is_featured=(img_data['type'] == 'hero')
            )
        
        print(f"Generated {len(images)} images for {article.title}")