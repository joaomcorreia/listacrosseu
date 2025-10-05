"""
Data Sources view for transparency page
"""
from django.shortcuts import render

def data_sources(request):
    """Data sources and transparency page"""
    
    sources = [
        {
            'name': 'OpenStreetMap',
            'url': 'https://openstreetmap.org',
            'license': 'Open Database License (ODbL)',
            'license_url': 'https://www.openstreetmap.org/copyright',
            'usage': 'Business locations, geographic coordinates, and point-of-interest data',
            'attribution': '© OpenStreetMap contributors',
            'commercial_use': True,
            'description': 'OpenStreetMap is a collaborative project to create a free editable map of the world. We use OSM data for business locations and geographic information with proper attribution.'
        },
        {
            'name': 'Eurostat',
            'url': 'https://ec.europa.eu/eurostat',
            'license': 'EU Copyright Notice',
            'license_url': 'https://ec.europa.eu/eurostat/web/main/about-us/policies/copyright',
            'usage': 'City population statistics and demographic data',
            'attribution': '© European Union, Eurostat',
            'commercial_use': True,
            'description': 'Eurostat provides official statistics for the European Union. We use their publicly available data for city demographics and population figures.'
        },
        {
            'name': 'GeoNames',
            'url': 'https://www.geonames.org',
            'license': 'Creative Commons Attribution 4.0',
            'license_url': 'https://creativecommons.org/licenses/by/4.0/',
            'usage': 'Geographic coordinates and place names',
            'attribution': '© GeoNames Project',
            'commercial_use': True,
            'description': 'GeoNames is a geographical database that covers all countries and contains over eleven million place names. We use this data for accurate geographic positioning.'
        },
        {
            'name': 'EU Publications Office',
            'url': 'https://publications.europa.eu',
            'license': 'EU Copyright Policy',
            'license_url': 'https://publications.europa.eu/en/web/about-us/legal-notices',
            'usage': 'Official EU business categories and regulatory information',
            'attribution': '© European Union',
            'commercial_use': True,
            'description': 'The EU Publications Office provides access to EU law, publications and other public documents. We reference their business classification systems.'
        },
        {
            'name': 'Business Owner Submissions',
            'url': None,
            'license': 'User Consent & Terms of Service',
            'license_url': '/terms/',
            'usage': 'Self-submitted business information from verified owners',
            'attribution': 'Business owners provide their own data',
            'commercial_use': True,
            'description': 'Business owners register themselves and provide their own business information. All submissions require email verification and explicit consent.'
        },
        {
            'name': 'Government Business Registries',
            'url': None,
            'license': 'Public Registry Data',
            'license_url': None,
            'usage': 'Official company registration data from 27 EU countries',
            'attribution': 'Various EU government agencies',
            'commercial_use': True,
            'description': 'We access publicly available business registry data from official government sources across EU member states, where legally permitted.'
        },
        {
            'name': 'Chamber of Commerce Partnerships',
            'url': None,
            'license': 'Partnership Agreements',
            'license_url': None,
            'usage': 'Member business listings from partner chambers',
            'attribution': 'Chamber of Commerce partnerships',
            'commercial_use': True,
            'description': 'We partner with local Chambers of Commerce to provide verified business listings of their members, with proper agreements in place.'
        }
    ]
    
    context = {
        'sources': sources,
        'total_sources': len(sources),
        'last_updated': '2025-10-05',
    }
    
    return render(request, 'businesses/data_sources.html', context)