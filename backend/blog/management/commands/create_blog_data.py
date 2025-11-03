from django.core.management.base import BaseCommand
from blog.models import BlogCategory, PricingPlan, BlogPost
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create initial blog data'

    def handle(self, *args, **options):
        # Create blog categories
        categories_data = [
            {
                'name': 'Business Tips',
                'slug': 'business-tips',
                'description': 'Helpful tips for running a successful business',
                'color': '#3B82F6'
            },
            {
                'name': 'EU Expansion',
                'slug': 'eu-expansion', 
                'description': 'Guides for expanding business across EU countries',
                'color': '#10B981'
            },
            {
                'name': 'Success Stories',
                'slug': 'success-stories',
                'description': 'Inspiring stories from successful EU businesses',
                'color': '#F59E0B'
            },
            {
                'name': 'Industry News',
                'slug': 'industry-news',
                'description': 'Latest news and trends across EU markets',
                'color': '#8B5CF6'
            },
            {
                'name': 'Legal & Compliance',
                'slug': 'legal-compliance',
                'description': 'EU regulations and compliance requirements',
                'color': '#EF4444'
            }
        ]

        for cat_data in categories_data:
            category, created = BlogCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f"Created category: {category.name}")

        # Create pricing plans
        plans_data = [
            {
                'name': 'Starter',
                'description': 'Perfect for new businesses just starting out',
                'price': 0,
                'currency': 'EUR',
                'billing_cycle': 'monthly',
                'features': [
                    '1 Business listing',
                    'Basic contact information',
                    'Community support',
                    'Mobile-friendly profile'
                ],
                'max_listings': 1,
                'max_images': 3,
                'priority_support': False,
                'is_active': True,
                'is_featured': False,
                'color_scheme': 'blue',
                'order': 1,
                'trial_days': 0
            },
            {
                'name': 'Professional',
                'description': 'For growing businesses that need more visibility',
                'price': 29.99,
                'currency': 'EUR',
                'billing_cycle': 'monthly',
                'features': [
                    'Up to 5 business listings',
                    'Enhanced business profiles',
                    'Priority listing placement',
                    'Analytics dashboard',
                    'Email support',
                    'Custom business hours',
                    'Photo gallery (up to 10 images per listing)'
                ],
                'max_listings': 5,
                'max_images': 10,
                'priority_support': False,
                'is_active': True,
                'is_featured': True,
                'color_scheme': 'green',
                'order': 2,
                'trial_days': 14
            },
            {
                'name': 'Enterprise',
                'description': 'Comprehensive solution for large businesses and franchises',
                'price': 99.99,
                'currency': 'EUR',
                'billing_cycle': 'monthly',
                'features': [
                    'Unlimited business listings',
                    'Premium business profiles',
                    'Top placement guarantee',
                    'Advanced analytics & insights',
                    'Priority phone & email support',
                    'API access for integrations',
                    'Custom branding options',
                    'Bulk listing management',
                    'Dedicated account manager'
                ],
                'max_listings': 999999,
                'max_images': 50,
                'priority_support': True,
                'is_active': True,
                'is_featured': False,
                'color_scheme': 'purple',
                'order': 3,
                'trial_days': 30
            }
        ]

        for plan_data in plans_data:
            plan, created = PricingPlan.objects.get_or_create(
                name=plan_data['name'],
                defaults=plan_data
            )
            if created:
                self.stdout.write(f"Created pricing plan: {plan.name}")

        # Create sample blog posts
        try:
            admin_user = User.objects.get(username='admin')
        except User.DoesNotExist:
            try:
                admin_user = User.objects.get(username='Joao')
            except User.DoesNotExist:
                admin_user = User.objects.create_user('blogadmin', 'blog@listacrosseu.com', 'password123')
                self.stdout.write("Created blog admin user")

        business_category = BlogCategory.objects.get(slug='business-tips')
        expansion_category = BlogCategory.objects.get(slug='eu-expansion')

        posts_data = [
            {
                'title': 'How to Start a Business in the European Union',
                'slug': 'how-to-start-business-eu-en',
                'author': admin_user,
                'language': 'en',
                'excerpt': 'A comprehensive guide to starting your business across EU member states, covering legal requirements, tax implications, and market opportunities.',
                'content': '''
# How to Start a Business in the European Union

Starting a business in the European Union offers incredible opportunities to access a market of over 450 million consumers. However, navigating the regulatory landscape and understanding the different business cultures across 27 member states can be challenging.

## Legal Requirements

Each EU country has its own business registration process, but there are common elements:

1. **Business Structure**: Choose between sole proprietorship, partnership, or corporation
2. **Registration**: Register with local business authorities
3. **Tax Registration**: Obtain tax identification numbers
4. **Permits and Licenses**: Industry-specific requirements vary by country

## Market Research

Before launching, conduct thorough market research:
- Analyze local competition
- Understand consumer preferences
- Research pricing strategies
- Identify cultural considerations

## Financial Planning

Secure adequate funding and understand:
- Initial capital requirements
- Ongoing operational costs
- Tax obligations in your chosen country
- Banking requirements for non-residents

## Next Steps

Ready to take the plunge? Consider starting with one country and expanding gradually. Our platform can help you connect with local business services and network with other entrepreneurs.
                ''',
                'category': expansion_category,
                'tags': 'business, startup, EU, legal, registration',
                'status': 'published',
                'featured': True,
                'meta_title': 'Start a Business in EU - Complete Guide 2024',
                'meta_description': 'Learn how to start your business in the European Union with our comprehensive guide covering legal, financial, and practical considerations.'
            },
            {
                'title': 'Cómo Iniciar un Negocio en la Unión Europea',
                'slug': 'como-iniciar-negocio-ue-es',
                'author': admin_user,
                'language': 'es',
                'excerpt': 'Una guía completa para iniciar tu negocio en los estados miembros de la UE, cubriendo requisitos legales, implicaciones fiscales y oportunidades de mercado.',
                'content': '''
# Cómo Iniciar un Negocio en la Unión Europea

Iniciar un negocio en la Unión Europea ofrece oportunidades increíbles para acceder a un mercado de más de 450 millones de consumidores. Sin embargo, navegar el panorama regulatorio y entender las diferentes culturas empresariales en 27 estados miembros puede ser desafiante.

## Requisitos Legales

Cada país de la UE tiene su propio proceso de registro empresarial, pero hay elementos comunes:

1. **Estructura Empresarial**: Elegir entre empresa individual, sociedad o corporación
2. **Registro**: Registrarse con las autoridades empresariales locales
3. **Registro Fiscal**: Obtener números de identificación fiscal
4. **Permisos y Licencias**: Los requisitos específicos de la industria varían por país

## Investigación de Mercado

Antes del lanzamiento, realiza una investigación exhaustiva del mercado:
- Analizar la competencia local
- Entender las preferencias del consumidor
- Investigar estrategias de precios
- Identificar consideraciones culturales

## Planificación Financiera

Asegurar financiación adecuada y entender:
- Requisitos de capital inicial
- Costos operativos continuos
- Obligaciones fiscales en tu país elegido
- Requisitos bancarios para no residentes

## Próximos Pasos

¿Listo para dar el salto? Considera comenzar con un país y expandirte gradualmente. Nuestra plataforma puede ayudarte a conectar con servicios empresariales locales y establecer contactos con otros emprendedores.
                ''',
                'category': expansion_category,
                'tags': 'negocio, startup, UE, legal, registro',
                'status': 'published',
                'featured': True,
                'meta_title': 'Iniciar Negocio en UE - Guía Completa 2024',
                'meta_description': 'Aprende cómo iniciar tu negocio en la Unión Europea con nuestra guía completa que cubre consideraciones legales, financieras y prácticas.'
            },
            {
                'title': '5 Essential Marketing Strategies for EU Businesses',
                'slug': 'marketing-strategies-eu-businesses-en',
                'author': admin_user,
                'language': 'en',
                'excerpt': 'Discover the most effective marketing strategies for reaching customers across European Union markets and building a strong brand presence.',
                'content': '''
# 5 Essential Marketing Strategies for EU Businesses

Marketing across the diverse European Union requires understanding cultural nuances, regulatory requirements, and consumer behaviors that vary significantly between member states.

## 1. Localized Content Marketing

Create content that resonates with local audiences:
- Translate content professionally
- Adapt messaging to cultural contexts
- Use local examples and references
- Understand regional humor and communication styles

## 2. Digital Presence Optimization

Ensure your online presence is optimized for each market:
- Local SEO for each country
- Country-specific social media platforms
- Localized website domains (.de, .fr, .es, etc.)
- Google My Business listings in local languages

## 3. Compliance with GDPR

Navigate European data protection regulations:
- Implement proper consent mechanisms
- Ensure data processing transparency
- Maintain audit trails
- Regular compliance reviews

## 4. Multi-Channel Approach

Diversify your marketing channels:
- Social media marketing (Facebook, Instagram, LinkedIn)
- Email marketing with local regulations compliance
- Traditional media where appropriate
- Influencer partnerships with local personalities

## 5. Customer Experience Localization

Adapt your customer experience:
- Local payment methods (SEPA, local cards)
- Regional customer service hours
- Culturally appropriate customer service styles
- Local return and refund policies

## Conclusion

Success in EU markets requires patience, cultural sensitivity, and a willingness to adapt your strategies to local preferences while maintaining brand consistency.
                ''',
                'category': business_category,
                'tags': 'marketing, EU, strategy, localization, digital',
                'status': 'published',
                'featured': False,
                'meta_title': 'EU Business Marketing Strategies - 5 Essential Tips',
                'meta_description': 'Master EU marketing with our 5 essential strategies covering localization, digital presence, compliance, and customer experience optimization.'
            }
        ]

        for post_data in posts_data:
            post, created = BlogPost.objects.get_or_create(
                slug=post_data['slug'],
                defaults=post_data
            )
            if created:
                self.stdout.write(f"Created blog post: {post.title}")

        self.stdout.write(self.style.SUCCESS('Successfully created initial blog data!'))