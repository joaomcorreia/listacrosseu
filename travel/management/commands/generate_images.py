from django.core.management.base import BaseCommand
from travel.image_generator import ImageGenerator
from travel.models import Article, ArticleImage


class Command(BaseCommand):
    help = 'Generate AI images for travel articles using MagicAI/OpenAI DALL-E'

    def add_arguments(self, parser):
        parser.add_argument(
            '--article-id',
            type=int,
            help='Generate images for specific article ID',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Generate images for all articles without images',
        )
        parser.add_argument(
            '--regenerate',
            action='store_true',
            help='Regenerate images even if they already exist',
        )

    def handle(self, *args, **options):
        generator = ImageGenerator()
        
        if options['article_id']:
            # Generate for specific article
            try:
                article = Article.objects.get(id=options['article_id'])
                self.generate_for_article(generator, article, options['regenerate'])
            except Article.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Article with ID {options["article_id"]} not found')
                )
                return
        
        elif options['all']:
            # Generate for all articles without images (or all if regenerate)
            if options['regenerate']:
                articles = Article.objects.filter(status='published')
            else:
                articles = Article.objects.filter(
                    status='published',
                    images__isnull=True
                ).distinct()
            
            self.stdout.write(f'Processing {articles.count()} articles...')
            
            for article in articles:
                self.generate_for_article(generator, article, options['regenerate'])
        
        else:
            self.stdout.write(
                self.style.ERROR('Please specify --article-id or --all')
            )

    def generate_for_article(self, generator, article, regenerate=False):
        """Generate images for a single article"""
        
        # Check if images already exist
        existing_images = article.images.count()
        if existing_images > 0 and not regenerate:
            self.stdout.write(
                f'Skipping {article.title} - already has {existing_images} images'
            )
            return
        
        if regenerate and existing_images > 0:
            # Delete existing images
            article.images.all().delete()
            self.stdout.write(f'Deleted {existing_images} existing images')
        
        self.stdout.write(f'Generating images for: {article.title}')
        
        try:
            images = generator.generate_article_images(article)
            
            # Save images to the article
            created_count = 0
            for img_data in images:
                ArticleImage.objects.create(
                    article=article,
                    image=img_data['path'],
                    caption=img_data['caption'],
                    alt_text=img_data['caption'],
                    is_featured=(img_data['type'] == 'hero'),
                    generated_by_ai=True,
                    generation_prompt=f"Travel image for {article.title}",
                    generation_style="photorealistic"
                )
                created_count += 1
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully generated {created_count} images for {article.title}'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error generating images for {article.title}: {e}')
            )