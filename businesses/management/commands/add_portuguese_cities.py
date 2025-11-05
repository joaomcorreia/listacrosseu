# businesses/management/commands/add_portuguese_cities.py
from django.core.management.base import BaseCommand
from businesses.models import Country, City, Category, Business
from accounts.models import CustomUser
from django.utils.text import slugify
import random

class Command(BaseCommand):
    help = 'Add more Portuguese cities with businesses and categories'

    def handle(self, *args, **options):
        # Get Portugal
        try:
            portugal = Country.objects.get(slug='portugal')
        except Country.DoesNotExist:
            self.stdout.write(self.style.ERROR('Portugal not found'))
            return

        # Get admin user as default owner
        try:
            admin_user = CustomUser.objects.get(username='admin')
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR('Admin user not found'))
            return

        # Additional Portuguese cities to add
        new_cities = [
            'Aveiro', 'Évora', 'Faro', 'Guimarães', 'Leiria',
            'Portimão', 'Santarém', 'Viseu', 'Viana do Castelo',
            'Torres Vedras', 'Caldas da Rainha', 'Cascais',
            'Sintra', 'Almada', 'Barreiro'
        ]

        # Business categories
        categories_data = [
            ('Restaurant', 'Restaurants and Food Services'),
            ('Technology', 'IT and Technology Services'),
            ('Tourism', 'Travel and Tourism'),
            ('Retail', 'Shopping and Retail'),
            ('Health', 'Healthcare and Medical'),
            ('Education', 'Schools and Training'),
            ('Finance', 'Banking and Financial Services'),
            ('Real Estate', 'Property and Real Estate'),
            ('Services', 'Professional Services'),
            ('Manufacturing', 'Industry and Manufacturing'),
            ('Construction', 'Building and Construction'),
            ('Transportation', 'Logistics and Transport'),
        ]

        # Create categories if they don't exist
        created_categories = []
        for name, description in categories_data:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'description': description, 'slug': slugify(name)}
            )
            created_categories.append(category)
            if created:
                self.stdout.write(f'Created category: {name}')

        # Business name templates by category
        business_templates = {
            'Restaurant': ['Restaurante {}', 'Tasca {}', 'Marisqueira {}', 'Pizzaria {}', 'Café {}'],
            'Technology': ['{} Tech', '{} Digital', '{} Software', 'Tech {}', '{} Solutions'],
            'Tourism': ['Hotel {}', 'Turismo {}', '{} Tours', 'Pousada {}', 'Quinta {}'],
            'Retail': ['Loja {}', '{} Store', 'Boutique {}', 'Mercado {}', '{} Shopping'],
            'Health': ['Clínica {}', 'Farmácia {}', 'Centro Médico {}', 'Laboratório {}', 'Fisio {}'],
            'Education': ['Escola {}', 'Centro de Formação {}', '{} Academy', 'Colégio {}', 'Instituto {}'],
            'Finance': ['Banco {}', 'Crédito {}', 'Seguros {}', 'Imobiliária {}', 'Investimentos {}'],
            'Real Estate': ['Imobiliária {}', '{} Properties', 'Mediação {}', '{} Realty', 'Casa {}'],
            'Services': ['Serviços {}', '{} Consulting', 'Assessoria {}', '{} Services', 'Apoio {}'],
            'Manufacturing': ['Fábrica {}', 'Indústria {}', '{} Manufacturing', 'Produção {}', '{} Industrial'],
            'Construction': ['Construção {}', '{} Obras', 'Engenharia {}', '{} Construction', 'Projetos {}'],
            'Transportation': ['Transportes {}', '{} Logistics', 'Mudanças {}', 'Frota {}', 'Entregas {}'],
        }

        added_cities = 0
        added_businesses = 0

        for city_name in new_cities:
            # Create city if it doesn't exist
            city, created = City.objects.get_or_create(
                name=city_name,
                country=portugal,
                defaults={'slug': slugify(city_name)}
            )
            
            if created:
                added_cities += 1
                self.stdout.write(f'Added city: {city_name}')

                # Add 6-12 businesses per city
                num_businesses = random.randint(6, 12)
                
                # Ensure we have at least 3 different categories
                selected_categories = random.sample(created_categories, min(6, len(created_categories)))
                
                for i in range(num_businesses):
                    category = random.choice(selected_categories)
                    templates = business_templates.get(category.name, ['{} Business'])
                    template = random.choice(templates)
                    
                    # Generate business name
                    business_name = template.format(city_name)
                    
                    # Add some variation to avoid duplicates
                    if random.choice([True, False]):
                        business_name += f' {random.choice(["Norte", "Sul", "Centro", "Central", "Premium", "Plus"])}'
                    
                    # Create business
                    business, created = Business.objects.get_or_create(
                        name=business_name,
                        city=city,
                        defaults={
                            'owner': admin_user,
                            'category': category,
                            'slug': slugify(business_name),
                            'verified': True,
                            'status': 'active',
                            'description': f'Quality {category.name.lower()} services in {city_name}, Portugal.',
                            'phone': f'+351 {random.randint(200000000, 299999999)}',
                            'email': f'info@{slugify(business_name)}.pt',
                            'address': f'Rua {random.choice(["da República", "de Camões", "Principal", "do Comércio"])} {random.randint(1, 200)}',
                        }
                    )
                    
                    if created:
                        added_businesses += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully added {added_cities} cities and {added_businesses} businesses to Portugal'
            )
        )
        
        # Show final stats
        total_cities = City.objects.filter(country=portugal).count()
        total_businesses = Business.objects.filter(city__country=portugal).count()
        
        self.stdout.write(f'Portugal now has {total_cities} cities and {total_businesses} businesses')