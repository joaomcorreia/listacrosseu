import pandas as pd
import json
import csv
import requests
from io import StringIO
from django.core.management.base import BaseCommand
from django.conf import settings
from businesses.models import Business, Category, Country, City
from data_import.models import DataSource, ImportJob, ImportRecord
from accounts.models import CustomUser


class DataImportService:
    """Service class for handling data imports from various sources"""
    
    def __init__(self, data_source):
        self.data_source = data_source
        self.errors = []
        self.success_count = 0
        self.error_count = 0
    
    def run_import(self, user=None):
        """Main method to run data import"""
        
        # Create import job
        job = ImportJob.objects.create(
            data_source=self.data_source,
            initiated_by=user
        )
        
        try:
            job.mark_started()
            
            # Get data based on source type
            if self.data_source.source_type == 'csv':
                data = self._import_from_csv()
            elif self.data_source.source_type == 'json':
                data = self._import_from_json()
            elif self.data_source.source_type == 'api':
                data = self._import_from_api()
            elif self.data_source.source_type == 'openstreetmap':
                data = self._import_from_openstreetmap()
            else:
                raise ValueError(f"Unsupported source type: {self.data_source.source_type}")
            
            job.total_records = len(data)
            job.save()
            
            # Process each record
            for item in data:
                try:
                    business = self._process_business_record(item, job)
                    if business:
                        self.success_count += 1
                        ImportRecord.objects.create(
                            import_job=job,
                            source_data=item,
                            status='success',
                            business=business
                        )
                    else:
                        self.error_count += 1
                        ImportRecord.objects.create(
                            import_job=job,
                            source_data=item,
                            status='skipped',
                            error_message='Business already exists or invalid data'
                        )
                    
                except Exception as e:
                    self.error_count += 1
                    ImportRecord.objects.create(
                        import_job=job,
                        source_data=item,
                        status='failed',
                        error_message=str(e)
                    )
                
                job.processed_records += 1
                job.successful_imports = self.success_count
                job.failed_imports = self.error_count
                job.save()
            
            job.mark_completed()
            
        except Exception as e:
            job.mark_failed(str(e))
            raise
        
        return job
    
    def _import_from_csv(self):
        """Import data from CSV file"""
        if not self.data_source.csv_file:
            raise ValueError("No CSV file provided")
        
        # Read CSV file
        df = pd.read_csv(self.data_source.csv_file.path)
        
        # Convert to list of dictionaries
        return df.to_dict('records')
    
    def _import_from_json(self):
        """Import data from JSON file"""
        if not self.data_source.json_file:
            raise ValueError("No JSON file provided")
        
        with open(self.data_source.json_file.path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle different JSON structures
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and 'data' in data:
            return data['data']
        elif isinstance(data, dict) and 'results' in data:
            return data['results']
        else:
            return [data]
    
    def _import_from_api(self):
        """Import data from API endpoint"""
        if not self.data_source.endpoint_url:
            raise ValueError("No API endpoint provided")
        
        headers = self.data_source.headers or {}
        if self.data_source.api_key:
            headers['Authorization'] = f"Bearer {self.data_source.api_key}"
        
        response = requests.get(self.data_source.endpoint_url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # Handle different API response structures
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and 'data' in data:
            return data['data']
        elif isinstance(data, dict) and 'results' in data:
            return data['results']
        else:
            return [data]
    
    def _import_from_openstreetmap(self):
        """Import data from OpenStreetMap using Overpass API"""
        
        # Example Overpass API query for restaurants in Europe
        overpass_query = """
        [out:json][timeout:25];
        (
          node["amenity"="restaurant"](40.0,-10.0,70.0,30.0);
          way["amenity"="restaurant"](40.0,-10.0,70.0,30.0);
          relation["amenity"="restaurant"](40.0,-10.0,70.0,30.0);
        );
        out center meta;
        """
        
        overpass_url = "http://overpass-api.de/api/interpreter"
        response = requests.post(overpass_url, data=overpass_query)
        response.raise_for_status()
        
        data = response.json()
        return data.get('elements', [])
    
    def _process_business_record(self, raw_data, job):
        """Process a single business record"""
        
        # Apply field mapping
        mapped_data = self._apply_field_mapping(raw_data)
        
        # Validate required fields
        if not self._validate_business_data(mapped_data):
            return None
        
        # Check for duplicates
        if self._is_duplicate(mapped_data):
            return None
        
        # Get or create related objects
        category = self._get_or_create_category(mapped_data.get('category'))
        country = self._get_or_create_country(mapped_data.get('country'))
        city = self._get_or_create_city(mapped_data.get('city'), country)
        
        # Create business
        business_data = {
            'name': mapped_data['name'],
            'description': mapped_data.get('description', ''),
            'email': mapped_data.get('email', ''),
            'phone': mapped_data.get('phone', ''),
            'website': mapped_data.get('website', ''),
            'address': mapped_data.get('address', ''),
            'city': city,
            'category': category,
            'latitude': mapped_data.get('latitude'),
            'longitude': mapped_data.get('longitude'),
            'plan': 'free',  # Default to free plan for imported businesses
            'status': 'active',  # Auto-approve imported businesses
        }
        
        # Create a default owner for imported businesses
        owner = self._get_import_user()
        business_data['owner'] = owner
        
        # Generate unique slug
        business_data['slug'] = self._generate_unique_slug(mapped_data['name'])
        
        business = Business.objects.create(**business_data)
        return business
    
    def _apply_field_mapping(self, raw_data):
        """Apply field mapping from source to business model"""
        mapped_data = {}
        field_mapping = self.data_source.field_mapping or {}
        
        for target_field, source_field in field_mapping.items():
            if source_field in raw_data:
                mapped_data[target_field] = raw_data[source_field]
            elif isinstance(source_field, dict) and 'path' in source_field:
                # Handle nested field access
                value = raw_data
                for key in source_field['path'].split('.'):
                    if isinstance(value, dict) and key in value:
                        value = value[key]
                    else:
                        value = None
                        break
                mapped_data[target_field] = value
        
        # Handle OpenStreetMap tags
        if 'tags' in raw_data:
            tags = raw_data['tags']
            if 'name' in tags:
                mapped_data['name'] = tags['name']
            if 'phone' in tags:
                mapped_data['phone'] = tags['phone']
            if 'website' in tags:
                mapped_data['website'] = tags['website']
            if 'addr:street' in tags or 'addr:housenumber' in tags:
                address_parts = []
                if 'addr:housenumber' in tags:
                    address_parts.append(tags['addr:housenumber'])
                if 'addr:street' in tags:
                    address_parts.append(tags['addr:street'])
                mapped_data['address'] = ' '.join(address_parts)
        
        # Handle coordinates for OpenStreetMap
        if 'lat' in raw_data and 'lon' in raw_data:
            mapped_data['latitude'] = raw_data['lat']
            mapped_data['longitude'] = raw_data['lon']
        
        return mapped_data
    
    def _validate_business_data(self, data):
        """Validate that business data has required fields"""
        required_fields = ['name']
        
        for field in required_fields:
            if not data.get(field):
                return False
        
        return True
    
    def _is_duplicate(self, data):
        """Check if business already exists"""
        name = data.get('name')
        email = data.get('email')
        
        if name and Business.objects.filter(name__iexact=name).exists():
            return True
        
        if email and Business.objects.filter(email__iexact=email).exists():
            return True
        
        return False
    
    def _get_or_create_category(self, category_name):
        """Get or create category"""
        if not category_name:
            category_name = "General"
        
        category, created = Category.objects.get_or_create(
            name__iexact=category_name,
            defaults={'name': category_name.title(), 'slug': category_name.lower().replace(' ', '-')}
        )
        return category
    
    def _get_or_create_country(self, country_name):
        """Get or create country"""
        if not country_name:
            country_name = "Unknown"
        
        country, created = Country.objects.get_or_create(
            name__iexact=country_name,
            defaults={'name': country_name, 'code': country_name[:2].upper()}
        )
        return country
    
    def _get_or_create_city(self, city_name, country):
        """Get or create city"""
        if not city_name:
            city_name = "Unknown"
        
        city, created = City.objects.get_or_create(
            name__iexact=city_name,
            country=country,
            defaults={'name': city_name}
        )
        return city
    
    def _get_import_user(self):
        """Get or create a user for imported businesses"""
        email = "imports@listacross.eu"
        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                'first_name': 'Data',
                'last_name': 'Import',
                'is_staff': True,
                'subscription_type': 'eu'
            }
        )
        return user
    
    def _generate_unique_slug(self, name):
        """Generate unique slug for business"""
        from django.utils.text import slugify
        
        base_slug = slugify(name)
        slug = base_slug
        counter = 1
        
        while Business.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        return slug


# Management command for running imports
class Command(BaseCommand):
    help = 'Import business data from various sources'
    
    def add_arguments(self, parser):
        parser.add_argument('--source', type=str, help='Data source name')
        parser.add_argument('--all', action='store_true', help='Import from all active sources')
    
    def handle(self, *args, **options):
        if options['all']:
            sources = DataSource.objects.filter(status='active')
        elif options['source']:
            sources = DataSource.objects.filter(name=options['source'])
        else:
            self.stdout.write(self.style.ERROR('Please specify --source or --all'))
            return
        
        for source in sources:
            self.stdout.write(f"Starting import from {source.name}...")
            
            try:
                import_service = DataImportService(source)
                job = import_service.run_import()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Import completed. Success: {job.successful_imports}, '
                        f'Failed: {job.failed_imports}'
                    )
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Import failed: {str(e)}'))