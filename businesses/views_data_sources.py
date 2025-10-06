"""
Data Sources view for transparency page
"""
from django.shortcuts import render

def data_sources(request):
    """Data sources and transparency page"""
    
    sources = [
        {
            'name': 'Platform Development Data',
            'url': None,
            'license': 'Proprietary',
            'license_url': None,
            'usage': 'Sample business listings for platform demonstration and testing',
            'attribution': 'ListAcross.eu Development Team',
            'commercial_use': True,
            'description': 'This is a development platform with sample business data created for demonstration purposes. The business listings are generated examples to showcase the platform\'s functionality and features.'
        },
        {
            'name': 'OpenStreetMap (Future Integration)',
            'url': 'https://openstreetmap.org',
            'license': 'Open Database License (ODbL)',
            'license_url': 'https://www.openstreetmap.org/copyright',
            'usage': 'Geographic data and business locations (planned integration)',
            'attribution': '© OpenStreetMap contributors',
            'commercial_use': True,
            'description': 'OpenStreetMap provides free geographic data. Our platform is designed to integrate with OSM data for accurate business locations and mapping functionality.'
        },
        {
            'name': 'EU Geographic References',
            'url': 'https://ec.europa.eu/eurostat',
            'license': 'EU Open Data Policy',
            'license_url': 'https://ec.europa.eu/info/legal-notice_en',
            'usage': 'EU country codes, city names, and geographic boundaries',
            'attribution': '© European Union',
            'commercial_use': True,
            'description': 'Official EU geographic data including country codes (ISO 3166-1) and major city names for accurate European coverage.'
        },
        {
            'name': 'Business Categories Framework',
            'url': 'https://ec.europa.eu/eurostat/web/nace',
            'license': 'EU Statistical Classification',
            'license_url': 'https://ec.europa.eu/eurostat/web/nace/methodology',
            'usage': 'Business category structure based on NACE classification',
            'attribution': '© European Union, Eurostat',
            'commercial_use': True,
            'description': 'Our business categories are structured following the NACE (Statistical Classification of Economic Activities) framework used across the European Union.'
        },
        {
            'name': 'User-Generated Content',
            'url': None,
            'license': 'Terms of Service Agreement',
            'license_url': '/terms/',
            'usage': 'Business registrations and owner-submitted information',
            'attribution': 'Individual business owners',
            'commercial_use': True,
            'description': 'Businesses can register on our platform and provide their own information. All user submissions are subject to verification and comply with our terms of service.'
        },
        {
            'name': 'Flag Icons',
            'url': 'https://flagicons.lipis.dev/',
            'license': 'MIT License',
            'license_url': 'https://github.com/lipis/flag-icons/blob/main/LICENSE',
            'usage': 'Country flag representations in navigation',
            'attribution': '© Panayiotis Lipiridis',
            'commercial_use': True,
            'description': 'High-quality SVG country flags used in our navigation and country selection interface, provided under MIT license.'
        }
    ]
    
    # Platform statistics
    from businesses.models import Business, City, Country, Category
    stats = {
        'businesses': Business.objects.count(),
        'cities': City.objects.count(),
        'countries': Country.objects.filter(is_active=True).count(),
        'categories': Category.objects.filter(parent__isnull=False).count(),
    }
    
    context = {
        'sources': sources,
        'total_sources': len(sources),
        'last_updated': '2025-10-06',
        'platform_stats': stats,
        'transparency_note': 'This platform is currently in development with sample data for demonstration purposes. All data sources are clearly identified and legally compliant.'
    }
    
    return render(request, 'businesses/data_sources.html', context)