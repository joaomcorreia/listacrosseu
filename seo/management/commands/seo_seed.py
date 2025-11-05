import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from seo.models import Country, Language, SeoPlan, SeoPage, SeoContentBlock


class Command(BaseCommand):
    help = 'Seed SEO module with initial data: languages, countries, plans, and example pages'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset existing data before seeding',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write(self.style.WARNING('Resetting existing SEO data...'))
            SeoContentBlock.objects.all().delete()
            SeoPage.objects.all().delete()
            SeoPlan.objects.all().delete()
            Country.objects.all().delete()
            Language.objects.all().delete()

        # Seed Languages
        self.stdout.write('Creating languages...')
        languages_data = [
            {'code': 'en', 'name': 'English'},
            {'code': 'fr', 'name': 'Français'},
            {'code': 'nl', 'name': 'Nederlands'},
            {'code': 'es', 'name': 'Español'},
            {'code': 'pt', 'name': 'Português'},
        ]
        
        for lang_data in languages_data:
            language, created = Language.objects.get_or_create(
                code=lang_data['code'],
                defaults={'name': lang_data['name']}
            )
            if created:
                self.stdout.write(f'  ✓ Created language: {language.name} ({language.code})')

        # Seed Countries (Core EU countries)
        self.stdout.write('Creating countries...')
        countries_data = [
            {'code': 'NL', 'name': 'Netherlands', 'default_locale': 'nl'},
            {'code': 'BE', 'name': 'Belgium', 'default_locale': 'nl'},
            {'code': 'FR', 'name': 'France', 'default_locale': 'fr'},
            {'code': 'DE', 'name': 'Germany', 'default_locale': 'de'},
            {'code': 'ES', 'name': 'Spain', 'default_locale': 'es'},
            {'code': 'PT', 'name': 'Portugal', 'default_locale': 'pt'},
            {'code': 'IT', 'name': 'Italy', 'default_locale': 'it'},
            {'code': 'AT', 'name': 'Austria', 'default_locale': 'de'},
            {'code': 'CH', 'name': 'Switzerland', 'default_locale': 'de'},
            {'code': 'LU', 'name': 'Luxembourg', 'default_locale': 'fr'},
        ]
        
        for country_data in countries_data:
            country, created = Country.objects.get_or_create(
                code=country_data['code'],
                defaults={
                    'name': country_data['name'],
                    'default_locale': country_data['default_locale']
                }
            )
            if created:
                self.stdout.write(f'  ✓ Created country: {country.name} ({country.code})')

        # Seed SEO Plans
        self.stdout.write('Creating SEO plans...')
        plans_data = [
            {
                'name': 'basic',
                'slug': 'basic',
                'order': 0,
                'features': {
                    'meta_tags': True,
                    'canonical_url': True,
                    'robots': True,
                    'image_alt': True,
                    'max_pages': 10
                }
            },
            {
                'name': 'growth',
                'slug': 'growth', 
                'order': 1,
                'features': {
                    'meta_tags': True,
                    'canonical_url': True,
                    'robots': True,
                    'image_alt': True,
                    'keywords': True,
                    'internal_links': True,
                    'sitemap': True,
                    'open_graph': True,
                    'twitter_cards': True,
                    'max_pages': 100
                }
            },
            {
                'name': 'premium',
                'slug': 'premium',
                'order': 2,
                'features': {
                    'meta_tags': True,
                    'canonical_url': True,
                    'robots': True,
                    'image_alt': True,
                    'keywords': True,
                    'internal_links': True,
                    'sitemap': True,
                    'open_graph': True,
                    'twitter_cards': True,
                    'json_ld': True,
                    'breadcrumbs': True,
                    'local_business_schema': True,
                    'service_schema': True,
                    'max_pages': 1000
                }
            }
        ]
        
        for plan_data in plans_data:
            plan, created = SeoPlan.objects.get_or_create(
                name=plan_data['name'],
                defaults={
                    'slug': plan_data['slug'],
                    'order': plan_data['order'],
                    'features': plan_data['features']
                }
            )
            if created:
                self.stdout.write(f'  ✓ Created plan: {plan.get_name_display()} (order: {plan.order})')

        # Get created objects for example pages
        en_lang = Language.objects.get(code='en')
        nl_lang = Language.objects.get(code='nl')
        pt_lang = Language.objects.get(code='pt')
        nl_country = Country.objects.get(code='NL')
        pt_country = Country.objects.get(code='PT')
        
        basic_plan = SeoPlan.objects.get(name='basic')
        growth_plan = SeoPlan.objects.get(name='growth')
        premium_plan = SeoPlan.objects.get(name='premium')

        # Create example pages
        self.stdout.write('Creating example SEO pages...')

        # 1. Global EN home page (Basic)
        home_page, created = SeoPage.objects.get_or_create(
            country=None,
            language=en_lang,
            slug='home',
            page_type='home',
            defaults={
                'plan': basic_plan,
                'meta_title': 'ListAcross EU - European Business Directory',
                'meta_description': 'Discover verified businesses across Europe. Connect with local services in 27 EU countries with our comprehensive multilingual directory.',
                'h1': 'Europe\'s Premier Business Directory',
                'h2': 'Connect with 6,593+ Verified European Businesses',
                'robots': 'index,follow',
                'image_alt_fallback': 'European business directory search interface',
                'is_published': True,
                'publish_at': timezone.now()
            }
        )
        
        if created:
            self.stdout.write('  ✓ Created global EN home page (Basic plan)')
            
            # Add content blocks
            SeoContentBlock.objects.create(
                seo_page=home_page,
                key='intro',
                content='<p>Welcome to ListAcross EU, your gateway to discovering quality businesses across all European Union countries. Our platform connects you with verified local services, from web design agencies to restaurants, in over 27 languages.</p>',
                order=1
            )

        # 2. NL country landing page (Growth)
        nl_page, created = SeoPage.objects.get_or_create(
            country=nl_country,
            language=nl_lang,
            slug='nederland',
            page_type='country',
            defaults={
                'plan': growth_plan,
                'meta_title': 'Nederlandse Bedrijven Directory - ListAcross EU',
                'meta_description': 'Ontdek geverifieerde Nederlandse bedrijven en diensten. Van webdesign tot lokale restaurants - vind de perfecte zakelijke partner in Nederland.',
                'h1': 'Nederlandse Bedrijvengids',
                'h2': 'Meer dan 126 geverifieerde Nederlandse bedrijven',
                'robots': 'index,follow',
                'image_alt_fallback': 'Nederlandse bedrijven zoekresultaten',
                'keywords_hint': 'Nederlandse bedrijven, Nederland directory, lokale diensten, zakelijke partners',
                'sitemap_include': True,
                'og_title': 'Nederlandse Bedrijven - ListAcross EU',
                'og_description': 'Vind de beste Nederlandse bedrijven en dienstverleners in onze uitgebreide directory.',
                'og_image_url': 'https://listacross.eu/images/netherlands-businesses.jpg',
                'twitter_card': 'summary_large_image',
                'internal_links': [
                    {'title': 'Amsterdam Bedrijven', 'href': '/nl/nl/amsterdam/'},
                    {'title': 'Rotterdam Diensten', 'href': '/nl/nl/rotterdam/'},
                    {'title': 'Den Haag Business', 'href': '/nl/nl/den-haag/'}
                ],
                'is_published': True,
                'publish_at': timezone.now()
            }
        )
        
        if created:
            self.stdout.write('  ✓ Created NL country page (Growth plan)')

        # 3. PT Porto webdesign service page (Premium with JSON-LD)
        service_page, created = SeoPage.objects.get_or_create(
            country=pt_country,
            language=pt_lang,
            slug='webdesign',
            page_type='service',
            defaults={
                'plan': premium_plan,
                'meta_title': 'Web Design Porto - Serviços Profissionais | ListAcross EU',
                'meta_description': 'Encontre os melhores serviços de web design no Porto. Designers profissionais para criar websites modernos e responsivos para sua empresa.',
                'h1': 'Serviços de Web Design no Porto',
                'h2': 'Designers Profissionais para Sua Empresa',
                'robots': 'index,follow',
                'image_alt_fallback': 'Web design services Porto Portugal',
                'keywords_hint': 'web design Porto, designers Porto, websites Portugal, desenvolvimento web',
                'sitemap_include': True,
                'og_title': 'Web Design Porto - Serviços Profissionais',
                'og_description': 'Descubra os melhores serviços de web design no Porto para sua empresa.',
                'og_image_url': 'https://listacross.eu/images/porto-web-design.jpg',
                'twitter_card': 'summary_large_image',
                'twitter_image_url': 'https://listacross.eu/images/porto-web-design-twitter.jpg',
                'breadcrumbs': [
                    {'name': 'Início', 'url': '/pt/'},
                    {'name': 'Portugal', 'url': '/pt/pt/'},
                    {'name': 'Porto', 'url': '/pt/pt/porto/'},
                    {'name': 'Web Design', 'url': '/pt/pt/porto/webdesign/'}
                ],
                'json_ld': json.dumps({
                    "@context": "https://schema.org",
                    "@type": "Service",
                    "name": "Serviços de Web Design Porto",
                    "description": "Serviços profissionais de web design no Porto, Portugal. Criação de websites modernos e responsivos.",
                    "provider": {
                        "@type": "Organization",
                        "name": "ListAcross EU"
                    },
                    "areaServed": {
                        "@type": "City",
                        "name": "Porto",
                        "addressCountry": "PT"
                    },
                    "serviceType": "Web Design",
                    "offers": {
                        "@type": "Offer",
                        "availability": "https://schema.org/InStock"
                    }
                }),
                'local_business_schema': {
                    "@type": "LocalBusiness",
                    "name": "Web Design Services Porto",
                    "address": {
                        "@type": "PostalAddress",
                        "addressLocality": "Porto",
                        "addressCountry": "PT"
                    }
                },
                'service_schema': {
                    "@type": "ProfessionalService",
                    "serviceType": "Web Design",
                    "areaServed": "Porto, Portugal"
                },
                'is_published': True,
                'publish_at': timezone.now()
            }
        )
        
        if created:
            self.stdout.write('  ✓ Created PT Porto webdesign service page (Premium plan)')
            
            # Add rich content blocks
            SeoContentBlock.objects.create(
                seo_page=service_page,
                key='features',
                content='<h3>Nossos Serviços de Web Design</h3><ul><li>Design Responsivo</li><li>SEO Otimizado</li><li>E-commerce Integration</li><li>CMS Personalizado</li></ul>',
                order=1
            )
            
            SeoContentBlock.objects.create(
                seo_page=service_page,
                key='cta',
                content='<div class="cta-section"><h3>Pronto para seu novo website?</h3><p>Conecte-se com os melhores designers de Porto através da nossa plataforma.</p></div>',
                order=2
            )

        # Summary
        self.stdout.write(self.style.SUCCESS('\n🎉 SEO seed data created successfully!'))
        self.stdout.write(f'  • Languages: {Language.objects.count()}')
        self.stdout.write(f'  • Countries: {Country.objects.count()}')
        self.stdout.write(f'  • SEO Plans: {SeoPlan.objects.count()}')
        self.stdout.write(f'  • SEO Pages: {SeoPage.objects.count()}')
        self.stdout.write(f'  • Content Blocks: {SeoContentBlock.objects.count()}')
        
        self.stdout.write('\n📋 Example pages created:')
        self.stdout.write('  • Global EN home (Basic): /en/')
        self.stdout.write('  • NL country page (Growth): /nl/nl/')
        self.stdout.write('  • PT Porto webdesign (Premium): /pt/pt/porto/webdesign/')
        
        self.stdout.write('\n🚀 Next steps:')
        self.stdout.write('  1. Visit /admin/seo/ to manage SEO pages')
        self.stdout.write('  2. Check /seo/dashboard/ for the custom dashboard')
        self.stdout.write('  3. Test API endpoints at /api/seo/api/pages/')
        self.stdout.write('  4. View sitemap at /api/seo/api/pages/sitemap/')