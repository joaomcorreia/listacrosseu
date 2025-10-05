# businesses/templatetags/map_tags.py
from django import template
from django.utils.safestring import mark_safe
from ..utils import get_countries_with_flags, generate_map_embed_url, get_map_coordinates

register = template.Library()

@register.inclusion_tag('includes/dynamic_map.html')
def dynamic_map(location_type='europe', location_code=None):
    """
    Render a dynamic map that zooms to the specified location
    Usage: {% dynamic_map 'country' 'AT' %} or {% dynamic_map 'city' 'porto' %}
    """
    map_url = generate_map_embed_url(location_type, location_code)
    coordinates = get_map_coordinates(location_type, location_code)
    
    return {
        'map_url': map_url,
        'coordinates': coordinates,
        'location_type': location_type,
        'location_code': location_code,
    }

@register.inclusion_tag('includes/flag_slider.html')
def flag_slider(show_all=True):
    """
    Render the infinite flag slider with all available countries
    Usage: {% flag_slider %} or {% flag_slider show_all=False %}
    """
    countries = get_countries_with_flags()
    
    # Sort countries alphabetically, but put EU flag first
    eu_flag = [c for c in countries if c['code'] == 'EU']
    other_countries = sorted([c for c in countries if c['code'] != 'EU'], 
                           key=lambda x: x['name'])
    
    all_countries = eu_flag + other_countries
    
    return {
        'countries': all_countries,
        'show_all': show_all,
    }

@register.simple_tag
def map_coordinates(location_type, location_code):
    """
    Get map coordinates as JSON for JavaScript use
    Usage: {% map_coordinates 'country' 'AT' %}
    """
    coords = get_map_coordinates(location_type, location_code)
    return mark_safe(f'{{"lat": {coords["lat"]}, "lng": {coords["lng"]}, "zoom": {coords["zoom"]}}}')

@register.filter
def country_url(country_code):
    """
    Generate URL for country page using slug
    Usage: {{ country.code|country_url }}
    """
    from businesses.models import Country
    try:
        country = Country.objects.get(code=country_code.upper())
        return f'/{country.slug}/'
    except Country.DoesNotExist:
        return f'/country/{country_code.lower()}/'

@register.filter 
def city_url(city_slug):
    """
    Generate URL for city page  
    Usage: {{ city.slug|city_url }}
    """
    return f'/city/{city_slug}/'