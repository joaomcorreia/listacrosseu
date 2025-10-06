from django.core.management.base import BaseCommand
from django.utils.text import slugify
from businesses.models import Business
import re

class Command(BaseCommand):
    help = 'Clean up business slugs to remove unnecessary suffixes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be changed without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        businesses = Business.objects.all()
        updated_count = 0
        
        self.stdout.write(f"Processing {businesses.count()} businesses...")
        
        for business in businesses:
            original_slug = business.slug
            
            # Create a clean slug from just the business name
            clean_name = business.name
            
            # Handle special characters
            clean_name = clean_name.replace('ç', 'c').replace('Ç', 'C')
            clean_name = clean_name.replace('á', 'a').replace('Á', 'A')
            clean_name = clean_name.replace('à', 'a').replace('À', 'A')
            clean_name = clean_name.replace('ã', 'a').replace('Ã', 'A')
            clean_name = clean_name.replace('é', 'e').replace('É', 'E')
            clean_name = clean_name.replace('ê', 'e').replace('Ê', 'E')
            clean_name = clean_name.replace('í', 'i').replace('Í', 'I')
            clean_name = clean_name.replace('ó', 'o').replace('Ó', 'O')
            clean_name = clean_name.replace('ô', 'o').replace('Ô', 'O')
            clean_name = clean_name.replace('õ', 'o').replace('Õ', 'O')
            clean_name = clean_name.replace('ú', 'u').replace('Ú', 'U')
            clean_name = clean_name.replace('ü', 'u').replace('Ü', 'U')
            
            # Remove special characters and create slug
            new_slug = slugify(clean_name)
            
            # If slug would be too short, add category
            if len(new_slug) < 3:
                new_slug = f"{new_slug}-{slugify(business.category.name)}"
            
            # Check for duplicates and add number if needed
            base_slug = new_slug
            counter = 1
            while Business.objects.filter(slug=new_slug).exclude(id=business.id).exists():
                new_slug = f"{base_slug}-{counter}"
                counter += 1
            
            if original_slug != new_slug:
                if dry_run:
                    self.stdout.write(
                        f"Would update '{business.name}': {original_slug} → {new_slug}"
                    )
                else:
                    business.slug = new_slug
                    business.save(update_fields=['slug'])
                    self.stdout.write(
                        self.style.SUCCESS(f"Updated '{business.name}': {original_slug} → {new_slug}")
                    )
                updated_count += 1
        
        if dry_run:
            self.stdout.write(f"\nDry run complete. Would update {updated_count} business slugs.")
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Successfully updated {updated_count} business slugs.")
            )