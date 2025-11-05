#!/usr/bin/env python
import os, sys, django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listacrosseu.settings')
django.setup()

from businesses.google_places_service import GooglePlacesService

service = GooglePlacesService('AIzaSyBmKk3uM1BZV_qTuodk9fQmYWLzp1J-k48')
results = service.search_places('restaurant Vila Nova de Gaia', 'Vila Nova de Gaia, Portugal')
if results:
    parsed = service.parse_place_data(results[0])
    print('Name:', parsed['name'])
    print('Latitude:', parsed['latitude'], 'type:', type(parsed['latitude']))
    print('Longitude:', parsed['longitude'], 'type:', type(parsed['longitude']))
    
    # Test rounding
    if parsed['latitude']:
        rounded_lat = round(float(parsed['latitude']), 6)
        print('Rounded lat:', rounded_lat)
    if parsed['longitude']:
        rounded_lng = round(float(parsed['longitude']), 6)  
        print('Rounded lng:', rounded_lng)