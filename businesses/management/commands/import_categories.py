"""
Management command to import business categories from CSV file.

Expected CSV format:
name,slug,description,icon,parent_slug,sort_order
Food & Dining,food-dining,Restaurants and dining establishments,🍽️,,1
Restaurants,restaurants,Full service restaurants,🍽️,food-dining,1
Fast Food,fast-food,Quick service restaurants,🍔,food-dining,2
Hotels & Accommodation,hotels,Lodging and accommodation,🏨,,2
"""

import csv
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify
from businesses.models import Category


class Command(BaseCommand):
    help = 'Import business categories from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be imported without actually importing',
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No data will be saved'))
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                categories_to_create = []
                categories_to_update = []
                errors = []
                
                # First pass: create parent categories
                parent_categories = {}
                rows_data = list(reader)
                
                for row_num, row in enumerate(rows_data, start=2):
                    try:
                        slug = row.get('slug', '').strip() or slugify(row['name'])
                        parent_slug = row.get('parent_slug', '').strip()
                        
                        category_data = {
                            'name': row['name'].strip(),
                            'slug': slug,
                            'description': row.get('description', '').strip(),
                            'icon': row.get('icon', '').strip(),
                            'sort_order': int(row.get('sort_order', 0)) if row.get('sort_order', '').strip() else 0,
                        }
                        
                        # Check if category exists
                        existing_category = Category.objects.filter(slug=slug).first()
                        
                        if not parent_slug:  # Parent category
                            if existing_category:
                                # Update existing
                                for key, value in category_data.items():
                                    setattr(existing_category, key, value)
                                existing_category.parent = None
                                categories_to_update.append(existing_category)
                                parent_categories[slug] = existing_category
                            else:
                                # Create new
                                new_category = Category(**category_data)
                                categories_to_create.append(new_category)
                                parent_categories[slug] = new_category
                        
                    except (ValueError, KeyError) as e:
                        errors.append(f"Row {row_num}: {str(e)}")
                        continue
                
                # Second pass: create child categories
                for row_num, row in enumerate(rows_data, start=2):
                    try:
                        slug = row.get('slug', '').strip() or slugify(row['name'])
                        parent_slug = row.get('parent_slug', '').strip()
                        
                        if parent_slug:  # Child category
                            category_data = {
                                'name': row['name'].strip(),
                                'slug': slug,
                                'description': row.get('description', '').strip(),
                                'icon': row.get('icon', '').strip(),
                                'sort_order': int(row.get('sort_order', 0)) if row.get('sort_order', '').strip() else 0,
                            }
                            
                            # Find parent
                            parent = parent_categories.get(parent_slug)
                            if not parent:
                                # Try to find existing parent in DB
                                try:
                                    parent = Category.objects.get(slug=parent_slug)
                                except Category.DoesNotExist:
                                    errors.append(f"Row {row_num}: Parent category '{parent_slug}' not found")
                                    continue
                            
                            category_data['parent'] = parent
                            
                            # Check if category exists
                            existing_category = Category.objects.filter(slug=slug).first()
                            
                            if existing_category:
                                # Update existing
                                for key, value in category_data.items():
                                    setattr(existing_category, key, value)
                                categories_to_update.append(existing_category)
                            else:
                                # Create new
                                categories_to_create.append(Category(**category_data))
                        
                    except (ValueError, KeyError) as e:
                        errors.append(f"Row {row_num}: {str(e)}")
                        continue
                
                # Display results
                self.stdout.write(f"Categories to create: {len(categories_to_create)}")
                self.stdout.write(f"Categories to update: {len(categories_to_update)}")
                
                if errors:
                    self.stdout.write(self.style.ERROR(f"Errors found ({len(errors)}):"))
                    for error in errors:
                        self.stdout.write(self.style.ERROR(f"  {error}"))
                
                if not dry_run and (categories_to_create or categories_to_update):
                    with transaction.atomic():
                        # Create new categories
                        if categories_to_create:
                            Category.objects.bulk_create(categories_to_create, ignore_conflicts=True)
                            self.stdout.write(
                                self.style.SUCCESS(f"Created {len(categories_to_create)} categories")
                            )
                        
                        # Update existing categories
                        for category in categories_to_update:
                            category.save()
                        if categories_to_update:
                            self.stdout.write(
                                self.style.SUCCESS(f"Updated {len(categories_to_update)} categories")
                            )
                
                elif dry_run:
                    self.stdout.write(self.style.WARNING('Dry run completed - no changes made'))
                    
        except FileNotFoundError:
            raise CommandError(f'File "{csv_file}" does not exist.')
        except Exception as e:
            raise CommandError(f'Error reading CSV file: {str(e)}')