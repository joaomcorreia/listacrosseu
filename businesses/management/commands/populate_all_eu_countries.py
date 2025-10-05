# businesses/management/commands/populate_all_eu_countries.py
from django.core.management.base import BaseCommand
from businesses.models import Country, City, Category, Business
from accounts.models import CustomUser
from django.utils.text import slugify
import random

class Command(BaseCommand):
    help = 'Populate all EU countries with cities and businesses'

    def handle(self, *args, **options):
        # Get admin user as default owner
        try:
            admin_user = CustomUser.objects.get(username='admin')
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR('Admin user not found'))
            return

        # EU countries with major cities (excluding Portugal which is already done)
        eu_countries_cities = {
            'Austria': ['Vienna', 'Salzburg', 'Innsbruck', 'Graz', 'Linz'],
            'Belgium': ['Brussels', 'Antwerp', 'Ghent', 'Charleroi', 'Liège', 'Bruges'],
            'Bulgaria': ['Sofia', 'Plovdiv', 'Varna', 'Burgas', 'Stara Zagora'],
            'Croatia': ['Zagreb', 'Split', 'Rijeka', 'Osijek', 'Zadar'],
            'Cyprus': ['Nicosia', 'Limassol', 'Larnaca', 'Paphos', 'Famagusta'],
            'Czech Republic': ['Prague', 'Brno', 'Ostrava', 'Plzen', 'Liberec'],
            'Denmark': ['Copenhagen', 'Aarhus', 'Odense', 'Aalborg', 'Esbjerg'],
            'Estonia': ['Tallinn', 'Tartu', 'Narva', 'Pärnu', 'Kohtla-Järve'],
            'Finland': ['Helsinki', 'Espoo', 'Tampere', 'Vantaa', 'Turku', 'Oulu'],
            'France': ['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice', 'Nantes', 'Strasbourg', 'Montpellier'],
            'Germany': ['Berlin', 'Hamburg', 'Munich', 'Cologne', 'Frankfurt', 'Stuttgart', 'Düsseldorf', 'Dortmund'],
            'Greece': ['Athens', 'Thessaloniki', 'Patras', 'Piraeus', 'Larissa'],
            'Hungary': ['Budapest', 'Debrecen', 'Szeged', 'Miskolc', 'Pécs'],
            'Ireland': ['Dublin', 'Cork', 'Limerick', 'Galway', 'Waterford'],
            'Italy': ['Rome', 'Milan', 'Naples', 'Turin', 'Palermo', 'Genoa', 'Bologna', 'Florence'],
            'Latvia': ['Riga', 'Daugavpils', 'Liepāja', 'Jelgava', 'Jūrmala'],
            'Lithuania': ['Vilnius', 'Kaunas', 'Klaipėda', 'Šiauliai', 'Panevėžys'],
            'Luxembourg': ['Luxembourg City', 'Esch-sur-Alzette', 'Dudelange', 'Differdange'],
            'Malta': ['Valletta', 'Birkirkara', 'Mosta', 'Qormi', 'Żabbar'],
            'Netherlands': ['Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht', 'Eindhoven', 'Tilburg'],
            'Poland': ['Warsaw', 'Kraków', 'Łódź', 'Wrocław', 'Poznań', 'Gdańsk', 'Szczecin'],
            'Romania': ['Bucharest', 'Cluj-Napoca', 'Timișoara', 'Iași', 'Constanța', 'Craiova'],
            'Slovakia': ['Bratislava', 'Košice', 'Prešov', 'Žilina', 'Banská Bystrica'],
            'Slovenia': ['Ljubljana', 'Maribor', 'Celje', 'Kranj', 'Velenje'],
            'Spain': ['Madrid', 'Barcelona', 'Valencia', 'Seville', 'Zaragoza', 'Málaga', 'Murcia', 'Palma'],
            'Sweden': ['Stockholm', 'Gothenburg', 'Malmö', 'Uppsala', 'Västerås', 'Örebro']
        }

        # Business categories
        main_categories = [
            'Restaurant', 'Technology', 'Tourism', 'Retail', 'Health', 'Education',
            'Finance', 'Real Estate', 'Services', 'Manufacturing', 'Construction', 'Transportation'
        ]

        # Create categories if they don't exist
        created_categories = []
        for cat_name in main_categories:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'description': f'{cat_name} services and businesses', 'slug': slugify(cat_name)}
            )
            created_categories.append(category)

        # Business name templates by category (language-neutral)
        business_templates = {
            'Restaurant': ['{} Restaurant', '{} Bistro', '{} Café', '{} Grill', '{} Kitchen'],
            'Technology': ['{} Tech', '{} Digital', '{} Software', '{} Solutions', '{} Systems'],
            'Tourism': ['Hotel {}', '{} Hotel', '{} Tours', '{} Travel', '{} Hospitality'],
            'Retail': ['{} Store', '{} Shop', '{} Market', '{} Trading', '{} Commerce'],
            'Health': ['{} Medical', '{} Health', '{} Clinic', '{} Care', '{} Wellness'],
            'Education': ['{} Academy', '{} Institute', '{} School', '{} Education', '{} Learning'],
            'Finance': ['{} Bank', '{} Finance', '{} Capital', '{} Investment', '{} Financial'],
            'Real Estate': ['{} Properties', '{} Realty', '{} Estates', '{} Housing', '{} Development'],
            'Services': ['{} Services', '{} Consulting', '{} Solutions', '{} Support', '{} Professional'],
            'Manufacturing': ['{} Industries', '{} Manufacturing', '{} Production', '{} Factory', '{} Works'],
            'Construction': ['{} Construction', '{} Building', '{} Engineering', '{} Projects', '{} Development'],
            'Transportation': ['{} Transport', '{} Logistics', '{} Shipping', '{} Moving', '{} Delivery'],
        }

        total_countries_added = 0
        total_cities_added = 0
        total_businesses_added = 0

        for country_name, cities in eu_countries_cities.items():
            try:
                country = Country.objects.get(name=country_name, is_active=True)
                self.stdout.write(f'Processing {country_name}...')
                
                cities_added = 0
                businesses_added = 0

                for city_name in cities:
                    # Create city if it doesn't exist
                    city, created = City.objects.get_or_create(
                        name=city_name,
                        country=country,
                        defaults={'slug': slugify(city_name)}
                    )
                    
                    # Add businesses regardless of whether city was just created or already existed
                    existing_businesses = Business.objects.filter(city=city).count()
                    
                    if created:
                        cities_added += 1
                        self.stdout.write(f'  Added city: {city_name}')
                    elif existing_businesses == 0:
                        self.stdout.write(f'  Adding businesses to existing city: {city_name}')

                    # Add businesses if city is new or has no businesses
                    if created or existing_businesses == 0:
                        # Add 8-15 businesses per city
                        num_businesses = random.randint(8, 15)
                        
                        # Ensure we have businesses in multiple categories
                        selected_categories = random.sample(created_categories, min(8, len(created_categories)))
                        
                        for i in range(num_businesses):
                            category = random.choice(selected_categories)
                            templates = business_templates.get(category.name, ['{} Business'])
                            template = random.choice(templates)
                            
                            # Generate business name
                            business_name = template.format(city_name)
                            
                            # Add some variation to avoid duplicates
                            suffixes = ['Central', 'Premium', 'Elite', 'Pro', 'Plus', 'Group', 'Company', 'Ltd']
                            if random.choice([True, False]):
                                business_name += f' {random.choice(suffixes)}'
                            
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
                                    'description': f'Quality {category.name.lower()} services in {city_name}, {country_name}.',
                                    'phone': f'+{random.randint(30, 99)} {random.randint(200000000, 999999999)}',
                                    'email': f'info@{slugify(business_name)[:20]}.com',
                                    'address': f'{random.choice(["Main Street", "Central Avenue", "Market Square", "Business District"])} {random.randint(1, 200)}',
                                }
                            )
                            
                            if created:
                                businesses_added += 1

                total_cities_added += cities_added
                total_businesses_added += businesses_added
                total_countries_added += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ {country_name}: {cities_added} cities, {businesses_added} businesses'
                    )
                )

            except Country.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'Country {country_name} not found in database, skipping...')
                )
                continue

        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 COMPLETED! Added to {total_countries_added} countries:'
                f'\n   Cities: {total_cities_added}'
                f'\n   Businesses: {total_businesses_added}'
            )
        )
        
        # Show final stats
        total_countries = Country.objects.filter(is_active=True).count()
        total_cities = City.objects.count()
        total_businesses = Business.objects.count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 TOTAL DATABASE STATS:'
                f'\n   Countries: {total_countries}'
                f'\n   Cities: {total_cities}'
                f'\n   Businesses: {total_businesses}'
            )
        )