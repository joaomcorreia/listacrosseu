"""
Management command to import cities from CSV file.

Expected CSV format:
name,country_code,latitude,longitude,population,is_capital
Paris,FR,48.8566,2.3522,2161000,True
Berlin,DE,52.5200,13.4050,3669491,True
Rome,IT,41.9028,12.4964,2873000,True
"""

import csv
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from businesses.models import City, Country


class Command(BaseCommand):
    help = 'Import cities from CSV file'

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
                
                cities_to_create = []
                cities_to_update = []
                errors = []
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Get country
                        try:
                            country = Country.objects.get(code=row['country_code'].upper())
                        except Country.DoesNotExist:
                            errors.append(f"Row {row_num}: Country '{row['country_code']}' not found")
                            continue
                        
                        # Parse data
                        city_data = {
                            'name': row['name'].strip(),
                            'country': country,
                            'latitude': float(row['latitude']) if row['latitude'].strip() else None,
                            'longitude': float(row['longitude']) if row['longitude'].strip() else None,
                            'population': int(row['population']) if row['population'].strip() else None,
                            'is_capital': row.get('is_capital', '').lower() in ['true', '1', 'yes'],
                        }
                        
                        # Check if city exists
                        existing_city = City.objects.filter(
                            name=city_data['name'], 
                            country=country
                        ).first()
                        
                        if existing_city:
                            # Update existing city
                            for key, value in city_data.items():
                                if key != 'country':  # Don't change country
                                    setattr(existing_city, key, value)
                            cities_to_update.append(existing_city)
                        else:
                            # Create new city
                            cities_to_create.append(City(**city_data))
                            
                    except (ValueError, KeyError) as e:
                        errors.append(f"Row {row_num}: {str(e)}")
                        continue
                
                # Display results
                self.stdout.write(f"Cities to create: {len(cities_to_create)}")
                self.stdout.write(f"Cities to update: {len(cities_to_update)}")
                
                if errors:
                    self.stdout.write(self.style.ERROR(f"Errors found ({len(errors)}):"))
                    for error in errors:
                        self.stdout.write(self.style.ERROR(f"  {error}"))
                
                if not dry_run and (cities_to_create or cities_to_update):
                    with transaction.atomic():
                        # Create new cities
                        if cities_to_create:
                            City.objects.bulk_create(cities_to_create, ignore_conflicts=True)
                            self.stdout.write(
                                self.style.SUCCESS(f"Created {len(cities_to_create)} cities")
                            )
                        
                        # Update existing cities
                        for city in cities_to_update:
                            city.save()
                        if cities_to_update:
                            self.stdout.write(
                                self.style.SUCCESS(f"Updated {len(cities_to_update)} cities")
                            )
                
                elif dry_run:
                    self.stdout.write(self.style.WARNING('Dry run completed - no changes made'))
                    
        except FileNotFoundError:
            raise CommandError(f'File "{csv_file}" does not exist.')
        except Exception as e:
            raise CommandError(f'Error reading CSV file: {str(e)}')