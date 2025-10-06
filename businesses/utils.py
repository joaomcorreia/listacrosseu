# businesses/utils.py
import os
from django.conf import settings
from django.contrib.staticfiles import finders
from .models import Country

def get_available_flags():
    """
    Automatically detect available flag files in static/assets/flags/
    Returns a list of country codes with available flags
    """
    flag_dir = os.path.join(settings.STATIC_ROOT or settings.BASE_DIR, 'static', 'assets', 'flags')
    if not os.path.exists(flag_dir):
        flag_dir = finders.find('assets/flags')
        if not flag_dir:
            return []
    
    available_flags = []
    try:
        for filename in os.listdir(flag_dir):
            if filename.endswith('.png'):
                country_code = filename.replace('.png', '').lower()
                available_flags.append(country_code)
    except (FileNotFoundError, TypeError):
        # Fallback to known flags
        available_flags = [
            'at', 'be', 'bg', 'hr', 'cy', 'cz', 'dk', 'ee', 'fi', 'fr', 'de', 
            'gr', 'hu', 'ie', 'it', 'lv', 'lt', 'lu', 'mt', 'nl', 'pl', 'pt', 
            'ro', 'sk', 'si', 'es', 'se', 'eu'
        ]
    
    return available_flags

def get_countries_with_flags():
    """
    Get all active EU countries with their flag information
    """
    from .models import Country
    
    countries_with_flags = []
    
    # Add EU flag first
    countries_with_flags.append({
        'code': 'EU',
        'name': 'European Union',
        'slug': '',
        'flag_url': 'assets/flags/eu.png'
    })
    
    # Get all active countries in alphabetical order
    countries = Country.objects.filter(is_active=True).order_by('name')
    
    for country in countries:
        # Use country code in lowercase for flag filename
        flag_code = country.code.lower()
        countries_with_flags.append({
            'code': country.code,
            'name': country.name,
            'slug': country.slug,
            'flag_url': f'assets/flags/{flag_code}.png'
        })
    
    return countries_with_flags

def get_map_coordinates(location_type, location_code):
    """
    Get map coordinates and zoom level for different location types
    """
    coordinates = {
        'europe': {
            'lat': 54.5260,
            'lng': 15.2551,
            'zoom': 4
        },
        # Country coordinates
        'countries': {
            'AT': {'lat': 47.5162, 'lng': 14.5501, 'zoom': 7},  # Austria
            'BE': {'lat': 50.8503, 'lng': 4.3517, 'zoom': 8},   # Belgium
            'BG': {'lat': 42.7339, 'lng': 25.4858, 'zoom': 7},  # Bulgaria
            'HR': {'lat': 45.1000, 'lng': 15.2000, 'zoom': 7},  # Croatia
            'CY': {'lat': 35.1264, 'lng': 33.4299, 'zoom': 9},  # Cyprus
            'CZ': {'lat': 49.8175, 'lng': 15.4730, 'zoom': 7},  # Czech Republic
            'DK': {'lat': 56.2639, 'lng': 9.5018, 'zoom': 7},   # Denmark
            'EE': {'lat': 58.5953, 'lng': 25.0136, 'zoom': 8},  # Estonia
            'FI': {'lat': 61.9241, 'lng': 25.7482, 'zoom': 6},  # Finland
            'FR': {'lat': 46.2276, 'lng': 2.2137, 'zoom': 6},   # France
            'DE': {'lat': 51.1657, 'lng': 10.4515, 'zoom': 6},  # Germany
            'GR': {'lat': 39.0742, 'lng': 21.8243, 'zoom': 7},  # Greece
            'HU': {'lat': 47.1625, 'lng': 19.5033, 'zoom': 7},  # Hungary
            'IE': {'lat': 53.1424, 'lng': -7.6921, 'zoom': 7},  # Ireland
            'IT': {'lat': 41.8719, 'lng': 12.5674, 'zoom': 6},  # Italy
            'LV': {'lat': 56.8796, 'lng': 24.6032, 'zoom': 8},  # Latvia
            'LT': {'lat': 55.1694, 'lng': 23.8813, 'zoom': 8},  # Lithuania
            'LU': {'lat': 49.8153, 'lng': 6.1296, 'zoom': 10},  # Luxembourg
            'MT': {'lat': 35.9375, 'lng': 14.3754, 'zoom': 11}, # Malta
            'NL': {'lat': 52.1326, 'lng': 5.2913, 'zoom': 8},   # Netherlands
            'PL': {'lat': 51.9194, 'lng': 19.1451, 'zoom': 6},  # Poland
            'PT': {'lat': 39.3999, 'lng': -8.2245, 'zoom': 7},  # Portugal
            'RO': {'lat': 45.9432, 'lng': 24.9668, 'zoom': 7},  # Romania
            'SK': {'lat': 48.6690, 'lng': 19.6990, 'zoom': 8},  # Slovakia
            'SI': {'lat': 46.1512, 'lng': 14.9955, 'zoom': 8},  # Slovenia
            'ES': {'lat': 40.4637, 'lng': -3.7492, 'zoom': 6},  # Spain
            'SE': {'lat': 60.1282, 'lng': 18.6435, 'zoom': 5},  # Sweden
        },
        # Major cities coordinates
        'cities': {
            'porto': {'lat': 41.1579, 'lng': -8.6291, 'zoom': 12},
            'lisbon': {'lat': 38.7223, 'lng': -9.1393, 'zoom': 12},
            'madrid': {'lat': 40.4168, 'lng': -3.7038, 'zoom': 12},
            'barcelona': {'lat': 41.3851, 'lng': 2.1734, 'zoom': 12},
            'paris': {'lat': 48.8566, 'lng': 2.3522, 'zoom': 12},
            'berlin': {'lat': 52.5200, 'lng': 13.4050, 'zoom': 12},
            'rome': {'lat': 41.9028, 'lng': 12.4964, 'zoom': 12},
            'amsterdam': {'lat': 52.3676, 'lng': 4.9041, 'zoom': 12},
            'vienna': {'lat': 48.2082, 'lng': 16.3738, 'zoom': 12},
            'prague': {'lat': 50.0755, 'lng': 14.4378, 'zoom': 12},
            'dublin': {'lat': 53.3498, 'lng': -6.2603, 'zoom': 12},
            'brussels': {'lat': 50.8503, 'lng': 4.3517, 'zoom': 12},
        }
    }
    
    if location_type == 'country':
        return coordinates['countries'].get(location_code.upper(), coordinates['europe'])
    elif location_type == 'city':
        return coordinates['cities'].get(location_code.lower(), coordinates['europe'])
    else:
        return coordinates['europe']

def generate_map_embed_url(location_type, location_code):
    """
    Generate Google Maps embed URL with proper zoom and center
    """
    coords = get_map_coordinates(location_type, location_code)
    
    base_url = "https://www.google.com/maps/embed/v1/view"
    api_key = "YOUR_GOOGLE_MAPS_API_KEY"  # You'll need to add this to settings
    
    # For development, use the iframe approach without API key
    params = f"!1m14!1m12!1m3!1d44136871.028996035!2d{coords['lng']}!3d{coords['lat']}!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1sen!2s!4v0000000000000"
    
    return f"https://www.google.com/maps/embed?pb={params}"