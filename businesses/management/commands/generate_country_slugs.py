# businesses/management/commands/generate_country_slugs.py
"""
Management command to generate slugs for existing countries
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from businesses.models import Country


class Command(BaseCommand):
    help = 'Generate slugs for existing countries'

    def handle(self, *args, **options):
        countries = Country.objects.all()
        
        for country in countries:
            if not country.slug:
                # Generate slug from country name
                base_slug = slugify(country.name.lower())
                
                # Ensure uniqueness
                slug = base_slug
                counter = 1
                while Country.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                country.slug = slug
                country.save()
                
                self.stdout.write(
                    self.style.SUCCESS(f'Generated slug "{slug}" for country: {country.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated slugs for {countries.count()} countries!')
        )