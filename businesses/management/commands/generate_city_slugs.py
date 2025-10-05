from django.core.management.base import BaseCommand
from businesses.models import City
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Generate slugs for all cities'
    
    def handle(self, *args, **options):
        cities = City.objects.all()
        
        for city in cities:
            if not city.slug:
                base_slug = slugify(f"{city.name}-{city.country.code}")
                city.slug = base_slug
                
                # Ensure uniqueness
                counter = 1
                while City.objects.filter(slug=city.slug).exclude(id=city.id).exists():
                    city.slug = f"{base_slug}-{counter}"
                    counter += 1
                
                city.save()
                self.stdout.write(f'Generated slug for {city.name}: {city.slug}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated slugs for {cities.count()} cities')
        )