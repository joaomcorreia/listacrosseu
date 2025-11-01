from django.core.management.base import BaseCommand
from geo.models import Country


class Command(BaseCommand):
    help = 'Seed EU countries with multilingual names'

    # EU countries with names in English, Dutch, and Portuguese
    EU_COUNTRIES = {
        'AT': {'en': 'Austria', 'nl': 'Oostenrijk', 'pt': 'Austria'},
        'BE': {'en': 'Belgium', 'nl': 'Belgie', 'pt': 'Belgica'},
        'BG': {'en': 'Bulgaria', 'nl': 'Bulgarije', 'pt': 'Bulgaria'},
        'HR': {'en': 'Croatia', 'nl': 'Kroatie', 'pt': 'Croacia'},
        'CY': {'en': 'Cyprus', 'nl': 'Cyprus', 'pt': 'Chipre'},
        'CZ': {'en': 'Czech Republic', 'nl': 'Tsjechie', 'pt': 'Republica Checa'},
        'DK': {'en': 'Denmark', 'nl': 'Denemarken', 'pt': 'Dinamarca'},
        'EE': {'en': 'Estonia', 'nl': 'Estland', 'pt': 'Estonia'},
        'FI': {'en': 'Finland', 'nl': 'Finland', 'pt': 'Finlandia'},
        'FR': {'en': 'France', 'nl': 'Frankrijk', 'pt': 'Franca'},
        'DE': {'en': 'Germany', 'nl': 'Duitsland', 'pt': 'Alemanha'},
        'GR': {'en': 'Greece', 'nl': 'Griekenland', 'pt': 'Grecia'},
        'HU': {'en': 'Hungary', 'nl': 'Hongarije', 'pt': 'Hungria'},
        'IE': {'en': 'Ireland', 'nl': 'Ierland', 'pt': 'Irlanda'},
        'IT': {'en': 'Italy', 'nl': 'Italie', 'pt': 'Italia'},
        'LV': {'en': 'Latvia', 'nl': 'Letland', 'pt': 'Letonia'},
        'LT': {'en': 'Lithuania', 'nl': 'Litouwen', 'pt': 'Lituania'},
        'LU': {'en': 'Luxembourg', 'nl': 'Luxemburg', 'pt': 'Luxemburgo'},
        'MT': {'en': 'Malta', 'nl': 'Malta', 'pt': 'Malta'},
        'NL': {'en': 'Netherlands', 'nl': 'Nederland', 'pt': 'Paises Baixos'},
        'PL': {'en': 'Poland', 'nl': 'Polen', 'pt': 'Polonia'},
        'PT': {'en': 'Portugal', 'nl': 'Portugal', 'pt': 'Portugal'},
        'RO': {'en': 'Romania', 'nl': 'Roemenie', 'pt': 'Romenia'},
        'SK': {'en': 'Slovakia', 'nl': 'Slowakije', 'pt': 'Eslovaquia'},
        'SI': {'en': 'Slovenia', 'nl': 'Slovenie', 'pt': 'Eslovenia'},
        'ES': {'en': 'Spain', 'nl': 'Spanje', 'pt': 'Espanha'},
        'SE': {'en': 'Sweden', 'nl': 'Zweden', 'pt': 'Suecia'},
    }

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for country_code, names in self.EU_COUNTRIES.items():
            country, created = Country.objects.get_or_create(
                code=country_code,
                defaults={
                    'names_json': names,
                    'is_active': True
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(f'Created country: {country_code} - {names["en"]}')
            else:
                # Update names if they've changed
                if country.names_json != names:
                    country.names_json = names
                    country.save()
                    updated_count += 1
                    self.stdout.write(f'Updated country: {country_code} - {names["en"]}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Countries seeded: {created_count} created, {updated_count} updated'
            )
        )