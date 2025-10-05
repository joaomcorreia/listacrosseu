"""
OpenStreetMap Business Data Collection Script
Completely legal and free to use for commercial projects
"""

import requests
import json
import csv
import time

class OSMBusinessCollector:
    def __init__(self):
        self.overpass_url = "http://overpass-api.de/api/interpreter"
        
    def get_businesses_by_city(self, city_name, country_code, category="amenity"):
        """
        Collect businesses from OpenStreetMap for a specific city
        Categories: amenity, shop, tourism, leisure, office
        """
        
        # Overpass QL query
        query = f"""
        [out:json][timeout:30];
        (
          area[name="{city_name}"][place~"city|town"]["ISO3166-1"="{country_code}"];
        )->.searchArea;
        (
          node[{category}](area.searchArea);
          way[{category}](area.searchArea);
          relation[{category}](area.searchArea);
        );
        out geom;
        """
        
        try:
            response = requests.post(self.overpass_url, data={'data': query})
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Request failed: {e}")
            return None
    
    def parse_business_data(self, osm_data):
        """Parse OSM data into business records"""
        businesses = []
        
        if not osm_data or 'elements' not in osm_data:
            return businesses
            
        for element in osm_data['elements']:
            if 'tags' not in element:
                continue
                
            tags = element['tags']
            
            # Extract business information
            business = {
                'name': tags.get('name', ''),
                'category': self.map_osm_category(tags),
                'address': self.build_address(tags),
                'phone': tags.get('phone', ''),
                'website': tags.get('website', ''),
                'email': tags.get('email', ''),
                'opening_hours': tags.get('opening_hours', ''),
                'latitude': self.get_lat(element),
                'longitude': self.get_lon(element),
                'osm_id': element.get('id', ''),
            }
            
            if business['name']:  # Only include named businesses
                businesses.append(business)
                
        return businesses
    
    def map_osm_category(self, tags):
        """Map OSM tags to our category system"""
        category_mapping = {
            'restaurant': 'restaurants',
            'fast_food': 'fast-food', 
            'cafe': 'cafes-coffee',
            'bar': 'bars-pubs',
            'pub': 'bars-pubs',
            'hotel': 'hotels',
            'hostel': 'hostels',
            'pharmacy': 'pharmacies',
            'bank': 'banks',
            'hospital': 'medical-centers',
            'dentist': 'dental-clinics',
            'shop': 'shopping',
            'supermarket': 'supermarkets',
            'bakery': 'bakeries',
            'hairdresser': 'hair-salons',
            'beauty': 'spas-wellness',
            'gym': 'fitness-centers',
            'library': 'libraries',
            'school': 'schools',
            'university': 'universities',
        }
        
        # Check different tag keys
        for key in ['amenity', 'shop', 'tourism', 'leisure']:
            if key in tags:
                osm_type = tags[key]
                return category_mapping.get(osm_type, 'services')
                
        return 'services'
    
    def build_address(self, tags):
        """Build address from OSM tags"""
        address_parts = []
        
        if 'addr:housenumber' in tags:
            address_parts.append(tags['addr:housenumber'])
        if 'addr:street' in tags:
            address_parts.append(tags['addr:street'])
            
        return ' '.join(address_parts) if address_parts else ''
    
    def get_lat(self, element):
        """Extract latitude from OSM element"""
        if element['type'] == 'node':
            return element.get('lat', '')
        elif 'center' in element:
            return element['center'].get('lat', '')
        return ''
    
    def get_lon(self, element):
        """Extract longitude from OSM element"""
        if element['type'] == 'node':
            return element.get('lon', '')
        elif 'center' in element:
            return element['center'].get('lon', '')
        return ''

def collect_businesses_for_cities():
    """Collect businesses for major EU cities"""
    collector = OSMBusinessCollector()
    
    cities = [
        ('Vienna', 'AT'), ('Amsterdam', 'NL'), ('Paris', 'FR'),
        ('Berlin', 'DE'), ('Rome', 'IT'), ('Barcelona', 'ES'),
        ('Prague', 'CZ'), ('Copenhagen', 'DK'), ('Budapest', 'HU'),
        ('Dublin', 'IE'), ('Brussels', 'BE'), ('Sofia', 'BG'),
    ]
    
    all_businesses = []
    
    for city, country in cities:
        print(f"Collecting businesses for {city}, {country}...")
        
        # Get different categories
        categories = ['amenity', 'shop', 'tourism', 'leisure', 'office']
        
        for category in categories:
            data = collector.get_businesses_by_city(city, country, category)
            if data:
                businesses = collector.parse_business_data(data)
                all_businesses.extend(businesses)
                print(f"  Found {len(businesses)} {category} businesses")
            
            time.sleep(1)  # Be nice to the API
    
    return all_businesses

if __name__ == "__main__":
    # This is 100% legal and free to use
    businesses = collect_businesses_for_cities()
    print(f"Total businesses collected: {len(businesses)}")
    
    # Save to CSV for import
    if businesses:
        with open('osm_businesses.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=businesses[0].keys())
            writer.writeheader()
            writer.writerows(businesses)
        print("Saved to osm_businesses.csv")