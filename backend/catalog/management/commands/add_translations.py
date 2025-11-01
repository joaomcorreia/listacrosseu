from django.core.management.base import BaseCommand
from catalog.models import Category


class Command(BaseCommand):
    help = 'Add German translations to categories'

    def handle(self, *args, **options):
        # German translations for common business categories
        translations = {
            'accounting-firms': {
                'de': 'Steuerberatungsfirmen',
                'fr': 'Cabinets comptables',
                'es': 'Firmas de contabilidad'
            },
            'art-galleries': {
                'de': 'Kunstgalerien',
                'fr': 'Galeries d\'art',
                'es': 'Galerías de arte'
            },
            'asian-restaurants': {
                'de': 'Asiatische Restaurants',
                'fr': 'Restaurants asiatiques',
                'es': 'Restaurantes asiáticos'
            },
            'auto-repair': {
                'de': 'Autoreparatur',
                'fr': 'Réparation automobile',
                'es': 'Reparación de autos'
            },
            'banks': {
                'de': 'Banken',
                'fr': 'Banques',
                'es': 'Bancos'
            },
            'beauty-salons': {
                'de': 'Schönheitssalons',
                'fr': 'Salons de beauté',
                'es': 'Salones de belleza'
            },
            'cafes': {
                'de': 'Cafés',
                'fr': 'Cafés',
                'es': 'Cafeterías'
            },
            'clothing-stores': {
                'de': 'Bekleidungsgeschäfte',
                'fr': 'Magasins de vêtements',
                'es': 'Tiendas de ropa'
            },
            'dental-clinics': {
                'de': 'Zahnkliniken',
                'fr': 'Cliniques dentaires',
                'es': 'Clínicas dentales'
            },
            'electronics-stores': {
                'de': 'Elektronikgeschäfte',
                'fr': 'Magasins d\'électronique',
                'es': 'Tiendas de electrónicos'
            },
            'fitness-centers': {
                'de': 'Fitnesszentren',
                'fr': 'Centres de fitness',
                'es': 'Centros de fitness'
            },
            'grocery-stores': {
                'de': 'Lebensmittelgeschäfte',
                'fr': 'Épiceries',
                'es': 'Tiendas de comestibles'
            },
            'hair-salons': {
                'de': 'Friseursalons',
                'fr': 'Salons de coiffure',
                'es': 'Salones de peluquería'
            },
            'hotels': {
                'de': 'Hotels',
                'fr': 'Hôtels',
                'es': 'Hoteles'
            },
            'insurance-agencies': {
                'de': 'Versicherungsagenturen',
                'fr': 'Agences d\'assurance',
                'es': 'Agencias de seguros'
            },
            'jewelry-stores': {
                'de': 'Juweliergeschäfte',
                'fr': 'Bijouteries',
                'es': 'Joyerías'
            },
            'law-firms': {
                'de': 'Anwaltskanzleien',
                'fr': 'Cabinets d\'avocats',
                'es': 'Bufetes de abogados'
            },
            'medical-clinics': {
                'de': 'Medizinische Kliniken',
                'fr': 'Cliniques médicales',
                'es': 'Clínicas médicas'
            },
            'pharmacies': {
                'de': 'Apotheken',
                'fr': 'Pharmacies',
                'es': 'Farmacias'
            },
            'real-estate': {
                'de': 'Immobilien',
                'fr': 'Immobilier',
                'es': 'Bienes raíces'
            },
            'restaurants': {
                'de': 'Restaurants',
                'fr': 'Restaurants',
                'es': 'Restaurantes'
            },
            'supermarkets': {
                'de': 'Supermärkte',
                'fr': 'Supermarchés',
                'es': 'Supermercados'
            },
            'travel-agencies': {
                'de': 'Reisebüros',
                'fr': 'Agences de voyage',
                'es': 'Agencias de viajes'
            },
            'veterinary-clinics': {
                'de': 'Tierkliniken',
                'fr': 'Cliniques vétérinaires',
                'es': 'Clínicas veterinarias'
            },
            'wedding-services': {
                'de': 'Hochzeitsservices',
                'fr': 'Services de mariage',
                'es': 'Servicios de boda'
            }
        }

        updated_count = 0
        
        for category_slug, langs in translations.items():
            try:
                category = Category.objects.get(slug=category_slug)
                
                # Update the names_json field with translations
                current_names = category.names_json or {}
                
                # Add the translations
                for lang_code, translation in langs.items():
                    current_names[lang_code] = translation
                
                # Keep existing English name if it exists
                if 'en' not in current_names:
                    current_names['en'] = category.slug.replace('-', ' ').title()
                
                category.names_json = current_names
                category.save()
                
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Updated translations for: {category_slug}')
                )
                
            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'Category not found: {category_slug}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} categories with translations')
        )