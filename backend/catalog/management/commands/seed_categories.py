from django.core.management.base import BaseCommand
from catalog.models import Category


class Command(BaseCommand):
    help = 'Seed starter categories with multilingual names'

    # Starter categories with names and synonyms
    CATEGORIES = {
        'restaurants': {
            'names': {'en': 'Restaurants', 'nl': 'Restaurants', 'pt': 'Restaurantes'},
            'synonyms': {'en': ['food', 'dining', 'eatery'], 'nl': ['eten', 'dineren'], 'pt': ['comida', 'jantar']}
        },
        'florists': {
            'names': {'en': 'Florists', 'nl': 'Bloemisten', 'pt': 'Floristas'},
            'synonyms': {'en': ['flowers', 'bouquets'], 'nl': ['bloemen'], 'pt': ['flores']}
        },
        'plumbers': {
            'names': {'en': 'Plumbers', 'nl': 'Loodgieters', 'pt': 'Canalizadores'},
            'synonyms': {'en': ['plumbing', 'pipes'], 'nl': ['loodgieterij'], 'pt': ['canalizacao']}
        },
        'electricians': {
            'names': {'en': 'Electricians', 'nl': 'Elektriciens', 'pt': 'Eletricistas'},
            'synonyms': {'en': ['electrical', 'wiring'], 'nl': ['elektra'], 'pt': ['eletrica']}
        },
        'hotels': {
            'names': {'en': 'Hotels', 'nl': 'Hotels', 'pt': 'Hoteis'},
            'synonyms': {'en': ['accommodation', 'lodging'], 'nl': ['accommodatie'], 'pt': ['hospedagem']}
        },
        'doctors': {
            'names': {'en': 'Doctors', 'nl': 'Artsen', 'pt': 'Medicos'},
            'synonyms': {'en': ['medical', 'physicians'], 'nl': ['medisch'], 'pt': ['medicina']}
        },
        'lawyers': {
            'names': {'en': 'Lawyers', 'nl': 'Advocaten', 'pt': 'Advogados'},
            'synonyms': {'en': ['legal', 'attorneys'], 'nl': ['juridisch'], 'pt': ['juridico']}
        },
        'hairdressers': {
            'names': {'en': 'Hairdressers', 'nl': 'Kappers', 'pt': 'Cabeleireiros'},
            'synonyms': {'en': ['hair salon', 'barbers'], 'nl': ['kapsalon'], 'pt': ['salao']}
        },
        'dentists': {
            'names': {'en': 'Dentists', 'nl': 'Tandartsen', 'pt': 'Dentistas'},
            'synonyms': {'en': ['dental'], 'nl': ['tandheelkunde'], 'pt': ['dental']}
        },
        'auto-repair': {
            'names': {'en': 'Auto Repair', 'nl': 'Auto Reparatie', 'pt': 'Reparacao Auto'},
            'synonyms': {'en': ['car repair', 'mechanics'], 'nl': ['garage'], 'pt': ['oficina']}
        },
    }

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for slug, data in self.CATEGORIES.items():
            category, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    'names_json': data['names'],
                    'synonyms_json': data['synonyms'],
                    'is_active': True
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(f'Created category: {slug} - {data["names"]["en"]}')
            else:
                # Update names and synonyms if they've changed
                updated = False
                if category.names_json != data['names']:
                    category.names_json = data['names']
                    updated = True
                if category.synonyms_json != data['synonyms']:
                    category.synonyms_json = data['synonyms']
                    updated = True
                
                if updated:
                    category.save()
                    updated_count += 1
                    self.stdout.write(f'Updated category: {slug} - {data["names"]["en"]}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Categories seeded: {created_count} created, {updated_count} updated'
            )
        )