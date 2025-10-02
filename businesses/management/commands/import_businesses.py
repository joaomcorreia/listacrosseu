"""
Management command to import businesses from CSV file.

Expected CSV format:
owner_email,name,slug,description,email,phone,website,address,city_name,country_code,postal_code,category_slug,plan,status,featured,verified
admin@listacrosseu.com,Restaurant Le Bernardin,le-bernardin,Fine French dining,contact@lebernardine.com,+33123456789,https://lebernardine.com,123 Rue de la Paix,Paris,FR,75001,restaurants,free,active,false,true
"""

import csv
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from businesses.models import Business, City, Country, Category

User = get_user_model()


class Command(BaseCommand):
    help = 'Import businesses from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be imported without actually importing',
        )
        parser.add_argument(
            '--default-owner',
            type=str,
            default='admin@listacrosseu.com',
            help='Default owner email if not specified in CSV',
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        dry_run = options['dry_run']
        default_owner_email = options['default_owner']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No data will be saved'))
        
        # Get default owner
        try:
            default_owner = User.objects.get(email=default_owner_email)
        except User.DoesNotExist:
            raise CommandError(f'Default owner "{default_owner_email}" not found. Create this user first.')
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                businesses_to_create = []
                businesses_to_update = []
                errors = []
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Get owner
                        owner_email = row.get('owner_email', '').strip() or default_owner_email
                        try:
                            owner = User.objects.get(email=owner_email)
                        except User.DoesNotExist:
                            owner = default_owner
                            self.stdout.write(f"Row {row_num}: Using default owner for {row['name']}")
                        
                        # Get city
                        city_name = row['city_name'].strip()
                        country_code = row['country_code'].upper().strip()
                        try:
                            city = City.objects.get(name=city_name, country__code=country_code)
                        except City.DoesNotExist:
                            errors.append(f"Row {row_num}: City '{city_name}' in '{country_code}' not found")
                            continue
                        
                        # Get category
                        category_slug = row['category_slug'].strip()
                        try:
                            category = Category.objects.get(slug=category_slug)
                        except Category.DoesNotExist:
                            errors.append(f"Row {row_num}: Category '{category_slug}' not found")
                            continue
                        
                        # Generate slug if not provided
                        slug = row.get('slug', '').strip() or slugify(row['name'])
                        
                        # Parse data
                        business_data = {
                            'owner': owner,
                            'name': row['name'].strip(),
                            'slug': slug,
                            'description': row.get('description', '').strip(),
                            'email': row.get('email', '').strip(),
                            'phone': row.get('phone', '').strip(),
                            'website': row.get('website', '').strip(),
                            'address': row.get('address', '').strip(),
                            'city': city,
                            'postal_code': row.get('postal_code', '').strip(),
                            'category': category,
                            'plan': row.get('plan', 'free').strip(),
                            'status': row.get('status', 'pending').strip(),
                            'featured': row.get('featured', '').lower() in ['true', '1', 'yes'],
                            'verified': row.get('verified', '').lower() in ['true', '1', 'yes'],
                        }
                        
                        # Optional fields
                        if row.get('short_description', '').strip():
                            business_data['short_description'] = row['short_description'].strip()
                        if row.get('latitude', '').strip():
                            business_data['latitude'] = float(row['latitude'])
                        if row.get('longitude', '').strip():
                            business_data['longitude'] = float(row['longitude'])
                        if row.get('meta_title', '').strip():
                            business_data['meta_title'] = row['meta_title'].strip()
                        if row.get('meta_description', '').strip():
                            business_data['meta_description'] = row['meta_description'].strip()
                        if row.get('keywords', '').strip():
                            business_data['keywords'] = row['keywords'].strip()
                        
                        # Business hours
                        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                            hours_key = f'{day}_hours'
                            if row.get(hours_key, '').strip():
                                business_data[hours_key] = row[hours_key].strip()
                        
                        # Check if business exists
                        existing_business = Business.objects.filter(slug=slug).first()
                        
                        if existing_business:
                            # Update existing business
                            for key, value in business_data.items():
                                setattr(existing_business, key, value)
                            businesses_to_update.append(existing_business)
                        else:
                            # Create new business
                            businesses_to_create.append(Business(**business_data))
                            
                    except (ValueError, KeyError) as e:
                        errors.append(f"Row {row_num}: {str(e)}")
                        continue
                
                # Display results
                self.stdout.write(f"Businesses to create: {len(businesses_to_create)}")
                self.stdout.write(f"Businesses to update: {len(businesses_to_update)}")
                
                if errors:
                    self.stdout.write(self.style.ERROR(f"Errors found ({len(errors)}):"))
                    for error in errors:
                        self.stdout.write(self.style.ERROR(f"  {error}"))
                
                if not dry_run and (businesses_to_create or businesses_to_update):
                    with transaction.atomic():
                        # Create new businesses
                        if businesses_to_create:
                            Business.objects.bulk_create(businesses_to_create, ignore_conflicts=True)
                            self.stdout.write(
                                self.style.SUCCESS(f"Created {len(businesses_to_create)} businesses")
                            )
                        
                        # Update existing businesses
                        for business in businesses_to_update:
                            business.save()
                        if businesses_to_update:
                            self.stdout.write(
                                self.style.SUCCESS(f"Updated {len(businesses_to_update)} businesses")
                            )
                
                elif dry_run:
                    self.stdout.write(self.style.WARNING('Dry run completed - no changes made'))
                    
        except FileNotFoundError:
            raise CommandError(f'File "{csv_file}" does not exist.')
        except Exception as e:
            raise CommandError(f'Error reading CSV file: {str(e)}')