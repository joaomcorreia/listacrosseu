"""
Management command to generate travel content using available AI providers
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from travel.models import Article, ArticleCategory, Tag
from accounts.models import CustomUser
from django.conf import settings


class Command(BaseCommand):
    help = 'Generate travel content using available AI providers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--provider',
            choices=['magicai', 'openai', 'auto'],
            default='auto',
            help='Choose AI provider (auto will try MagicAI first, then OpenAI)'
        )
        parser.add_argument(
            '--city',
            type=str,
            help='Generate content for specific city'
        )
        parser.add_argument(
            '--test-openai',
            action='store_true',
            help='Test direct OpenAI integration'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 AI Content Generation Started')
        )
        
        if options['test_openai']:
            self.test_openai()
            return
        
        if options['city']:
            self.generate_city_content(options['city'], options['provider'])
        else:
            self.show_available_providers()

    def test_openai(self):
        """Test direct OpenAI integration"""
        self.stdout.write('\n🔍 Testing Direct OpenAI Integration...')
        
        openai_key = getattr(settings, 'OPENAI_API_KEY', '')
        
        if not openai_key:
            self.stdout.write(
                self.style.ERROR('❌ No OpenAI API key found. Add OPENAI_API_KEY to your .env file.')
            )
            return
        
        try:
            from travel.openai_direct import DirectOpenAIClient
            
            client = DirectOpenAIClient()
            
            # Test with a simple generation
            result = client.generate_city_guide("Hamburg", "Germany")
            
            if result.get('success'):
                self.stdout.write(
                    self.style.SUCCESS('✅ OpenAI integration working!')
                )
                self.stdout.write(f"Generated content length: {len(result.get('content', ''))} characters")
                self.stdout.write(f"Title: {result.get('title', 'N/A')}")
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ OpenAI test failed: {result.get("error", "Unknown error")}')
                )
                
        except ImportError:
            self.stdout.write(
                self.style.ERROR('❌ OpenAI library not installed. Run: pip install openai')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ OpenAI test error: {str(e)}')
            )

    def generate_city_content(self, city_name, provider):
        """Generate content for a specific city"""
        self.stdout.write(f'\n🏙️ Generating content for {city_name}...')
        
        # Get admin user
        try:
            admin_user = CustomUser.objects.get(email='admin@listacrosseu.com')
        except CustomUser.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('❌ Admin user not found.')
            )
            return
        
        # Get category and tag
        category, _ = ArticleCategory.objects.get_or_create(
            name='City Guides',
            defaults={'description': 'AI-generated city guides'}
        )
        
        tag, _ = Tag.objects.get_or_create(
            name='AI Generated',
            defaults={'color': '#28a745'}
        )
        
        # Try different providers based on selection
        content_generated = False
        
        if provider in ['auto', 'magicai']:
            content_generated = self._try_magicai_generation(
                city_name, admin_user, category, tag
            )
        
        if not content_generated and provider in ['auto', 'openai']:
            content_generated = self._try_openai_generation(
                city_name, admin_user, category, tag
            )
        
        if not content_generated:
            self.stdout.write(
                self.style.ERROR('❌ No AI providers available. Please configure API keys.')
            )

    def _try_magicai_generation(self, city_name, admin_user, category, tag):
        """Try generating content with MagicAI"""
        try:
            from travel.magicai_integration import MagicAIClient
            
            if not getattr(settings, 'MAGICAI_API_KEY', ''):
                self.stdout.write('⚠️ MagicAI API key not configured, skipping...')
                return False
            
            self.stdout.write('🤖 Trying MagicAI...')
            
            client = MagicAIClient()
            result = client.generate_city_guide(city_name, "Europe")
            
            if result.get('success'):
                article = Article.objects.create(
                    title=result.get('title', f'{city_name} Travel Guide'),
                    subtitle=f'Discover the best of {city_name}',
                    excerpt=result.get('content', '')[:200] + '...',
                    content=result.get('content', ''),
                    article_type='guide',
                    category=category,
                    status='draft',
                    author=admin_user,
                    meta_description=result.get('content', '')[:160] + '...'
                )
                article.tags.add(tag)
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Created article with MagicAI: {article.title} (ID: {article.id})')
                )
                return True
            else:
                self.stdout.write(f'❌ MagicAI failed: {result.get("error", "")}')
                return False
                
        except Exception as e:
            self.stdout.write(f'❌ MagicAI error: {str(e)}')
            return False

    def _try_openai_generation(self, city_name, admin_user, category, tag):
        """Try generating content with direct OpenAI"""
        try:
            from travel.openai_direct import DirectOpenAIClient
            
            if not getattr(settings, 'OPENAI_API_KEY', ''):
                self.stdout.write('⚠️ OpenAI API key not configured, skipping...')
                return False
            
            self.stdout.write('🧠 Trying Direct OpenAI...')
            
            client = DirectOpenAIClient()
            result = client.generate_city_guide(city_name, "Europe")
            
            if result.get('success'):
                article = Article.objects.create(
                    title=result.get('title', f'{city_name} Travel Guide'),
                    subtitle=f'AI-generated guide to {city_name}',
                    excerpt=result.get('content', '')[:200] + '...',
                    content=result.get('content', ''),
                    article_type='guide',
                    category=category,
                    status='draft',
                    author=admin_user,
                    meta_description=result.get('content', '')[:160] + '...'
                )
                article.tags.add(tag)
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Created article with OpenAI: {article.title} (ID: {article.id})')
                )
                return True
            else:
                self.stdout.write(f'❌ OpenAI failed: {result.get("error", "")}')
                return False
                
        except Exception as e:
            self.stdout.write(f'❌ OpenAI error: {str(e)}')
            return False

    def show_available_providers(self):
        """Show which AI providers are configured"""
        self.stdout.write('\n📋 Available AI Providers:')
        
        magicai_key = getattr(settings, 'MAGICAI_API_KEY', '')
        openai_key = getattr(settings, 'OPENAI_API_KEY', '')
        
        if magicai_key:
            self.stdout.write('✅ MagicAI (via tools.justcodeworks.net)')
        else:
            self.stdout.write('❌ MagicAI - API key not configured')
        
        if openai_key:
            self.stdout.write('✅ Direct OpenAI')
        else:
            self.stdout.write('❌ Direct OpenAI - API key not configured')
        
        if not magicai_key and not openai_key:
            self.stdout.write('\n💡 To get started:')
            self.stdout.write('   1. Add OPENAI_API_KEY to your .env file (easiest)')
            self.stdout.write('   2. Or find MagicAI API key in your dashboard')
            self.stdout.write('\n🧪 Test OpenAI: python manage.py generate_content --test-openai')
            self.stdout.write('🏙️ Generate content: python manage.py generate_content --city Hamburg')