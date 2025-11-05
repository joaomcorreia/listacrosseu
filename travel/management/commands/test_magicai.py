"""
Management command to test and generate content using MagicAI integration
"""
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from travel.models import Article, ArticleCategory, Tag, TravelItinerary, ItineraryDay
from businesses.models import City, Country
from accounts.models import CustomUser
from travel.magicai_integration import MagicAIClient, auto_generate_article_content
import json


class Command(BaseCommand):
    help = 'Test MagicAI integration and generate sample travel content'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test-connection',
            action='store_true',
            help='Test connection to MagicAI API'
        )
        parser.add_argument(
            '--generate-articles',
            action='store_true',
            help='Generate sample articles using MagicAI'
        )
        parser.add_argument(
            '--city',
            type=str,
            help='Generate content for specific city'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be generated without saving'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 MagicAI Integration Test Started')
        )
        
        # Initialize MagicAI client
        client = MagicAIClient()
        
        if options['test_connection']:
            self.test_api_connection(client)
        
        if options['generate_articles']:
            self.generate_sample_articles(client, options)
        
        if options['city']:
            self.generate_city_content(client, options['city'], options.get('dry_run', False))

    def test_api_connection(self, client):
        """Test basic connection to MagicAI API"""
        self.stdout.write('\n🔍 Testing MagicAI API Connection...')
        
        try:
            # Test with a simple content generation
            result = client._generate_content(
                template='article-generator',
                prompt='Write a short paragraph about travel in Europe.',
                title='API Test'
            )
            
            if result.get('success'):
                self.stdout.write(
                    self.style.SUCCESS('✅ MagicAI API connection successful!')
                )
                self.stdout.write(f"Sample response: {result.get('content', '')[:100]}...")
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ API connection failed: {result.get("error", "Unknown error")}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Connection test failed: {str(e)}')
            )

    def generate_sample_articles(self, client, options):
        """Generate sample articles for major European cities"""
        self.stdout.write('\n📝 Generating Sample Travel Articles...')
        
        # Get or create admin user
        try:
            admin_user = CustomUser.objects.get(email='admin@listacrosseu.com')
        except CustomUser.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('❌ Admin user not found. Please create admin user first.')
            )
            return
        
        # Get or create category and tag
        category, _ = ArticleCategory.objects.get_or_create(
            name='City Guides',
            defaults={'description': 'Comprehensive guides to European cities'}
        )
        
        tag, _ = Tag.objects.get_or_create(
            name='Must See',
            defaults={'color': '#007bff'}
        )
        
        # Sample cities to generate content for
        sample_cities = [
            ('Hamburg', 'Germany'),
            ('Barcelona', 'Spain'), 
            ('Amsterdam', 'Netherlands'),
            ('Vienna', 'Austria'),
            ('Prague', 'Czech Republic')
        ]
        
        for city_name, country_name in sample_cities:
            self.stdout.write(f'\n🏙️  Generating content for {city_name}, {country_name}...')
            
            if options.get('dry_run'):
                self.stdout.write(f'   [DRY RUN] Would generate article for {city_name}')
                continue
            
            try:
                # Generate content using MagicAI
                result = client.generate_city_guide(
                    city_name=city_name,
                    country=country_name,
                    language='en'
                )
                
                if result.get('success'):
                    # Create article
                    article = Article.objects.create(
                        title=result.get('title', f'Complete {city_name} Travel Guide 2025'),
                        subtitle=f'Discover the best of {city_name}',
                        excerpt=result.get('content', '')[:200] + '...',
                        content=result.get('content', ''),
                        article_type='guide',
                        category=category,
                        status='published',
                        author=admin_user,
                        published_at=timezone.now(),
                        featured=True,
                        seo_title=result.get('title', ''),
                        meta_description=result.get('content', '')[:160] + '...'
                    )
                    
                    article.tags.add(tag)
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'   ✅ Created article: {article.title}')
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f'   📊 Tokens used: {result.get("tokens_used", "N/A")}')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'   ❌ Failed to generate content: {result.get("error", "Unknown error")}')
                    )
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'   ❌ Error generating {city_name} content: {str(e)}')
                )

    def generate_city_content(self, client, city_name, dry_run=False):
        """Generate content for a specific city"""
        self.stdout.write(f'\n🎯 Generating content for {city_name}...')
        
        if dry_run:
            self.stdout.write(f'[DRY RUN] Would generate comprehensive content for {city_name}')
            return
        
        try:
            # Generate city guide
            guide_result = client.generate_city_guide(
                city_name=city_name,
                country="Europe",  # Generic for now
                language='en'
            )
            
            if guide_result.get('success'):
                self.stdout.write('✅ Generated city guide content')
                self.stdout.write(f"Title: {guide_result.get('title', 'N/A')}")
                self.stdout.write(f"Content length: {len(guide_result.get('content', ''))} characters")
                
                # Generate itinerary
                itinerary_result = client.generate_travel_itinerary(
                    destination=city_name,
                    duration_days=3,
                    travel_style='cultural'
                )
                
                if itinerary_result.get('success'):
                    self.stdout.write('✅ Generated 3-day itinerary')
                    self.stdout.write(f"Itinerary length: {len(itinerary_result.get('content', ''))} characters")
                else:
                    self.stdout.write(f'❌ Failed to generate itinerary: {itinerary_result.get("error", "")}')
            else:
                self.stdout.write(f'❌ Failed to generate city guide: {guide_result.get("error", "")}')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {str(e)}')
            )

    def show_sample_prompts(self):
        """Show sample prompts that can be used with MagicAI"""
        self.stdout.write('\n📋 Sample MagicAI Prompts for Travel Content:')
        
        prompts = {
            'City Guide': '''
            Write a comprehensive travel guide for [CITY], [COUNTRY].
            Include: attractions, restaurants, transportation, accommodation, culture, safety tips.
            Target: 2000-3000 words, SEO-optimized.
            ''',
            'Restaurant Review': '''
            Write a detailed restaurant review for [RESTAURANT] in [CITY].
            Include: atmosphere, menu highlights, price range, service, recommendations.
            Style: Food blogger, engaging tone.
            ''',
            'Attraction Guide': '''
            Write about [ATTRACTION] in [CITY].
            Include: history, what to expect, visiting tips, nearby attractions, photography tips.
            Make it inspiring and informative.
            ''',
            'Travel Itinerary': '''
            Create a [X]-day itinerary for [DESTINATION].
            Include: daily activities, restaurants, transportation, costs, alternatives.
            Style: [budget/luxury/cultural/adventure]
            '''
        }
        
        for prompt_type, prompt_text in prompts.items():
            self.stdout.write(f'\n🔹 {prompt_type}:')
            self.stdout.write(f'   {prompt_text.strip()}')