# businesses/management/commands/regenerate_city_slugs.py

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from businesses.models import City


class Command(BaseCommand):
    help = 'Regenerate clean city slugs without country codes'

    def handle(self, *args, **options):
        cities = City.objects.all()
        updated_count = 0
        
        self.stdout.write(f'Regenerating slugs for {cities.count()} cities...')
        
        for city in cities:
            old_slug = city.slug
            
            # Generate clean slug from city name only
            base_slug = slugify(city.name.lower())
            new_slug = base_slug
            
            # Ensure uniqueness within the same country
            counter = 1
            while City.objects.filter(slug=new_slug, country=city.country).exclude(pk=city.pk).exists():
                new_slug = f"{base_slug}-{counter}"
                counter += 1
            
            if old_slug != new_slug:
                city.slug = new_slug
                city.save(update_fields=['slug'])
                self.stdout.write(
                    self.style.SUCCESS(f'Updated {city.name}, {city.country.name}: {old_slug} → {new_slug}')
                )
                updated_count += 1
            else:
                self.stdout.write(f'No change for {city.name}, {city.country.name}: {city.slug}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} city slugs')
        )