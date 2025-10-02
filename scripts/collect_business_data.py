"""
EU Business Data Collection Script
This script collects business data from various free sources across EU countries.

Dependencies to install:
pip install requests beautifulsoup4 pandas geopy overpy selenium webdriver-manager

Usage:
python collect_business_data.py --country AT --city Vienna --limit 100
"""

import requests
import json
import pandas as pd
import time
from typing import List, Dict, Optional
import argparse
from dataclasses import dataclass, asdict
from geopy.geocoders import Nominatim
import overpy
import csv
import os
from urllib.parse import urlencode, quote

@dataclass
class BusinessData:
    name: str
    category: str
    address: str
    city: str
    country: str
    country_code: str
    phone: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    opening_hours: Optional[Dict] = None
    source: str = "OpenStreetMap"

class EUBusinessCollector:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="listacrosseu-collector")
        self.api = overpy.Overpass()
        
        # EU countries with their codes and major cities
        self.eu_countries = {
            'AT': {'name': 'Austria', 'cities': ['Vienna', 'Salzburg', 'Innsbruck', 'Graz', 'Linz']},
            'BE': {'name': 'Belgium', 'cities': ['Brussels', 'Antwerp', 'Ghent', 'Charleroi', 'Liège']},
            'BG': {'name': 'Bulgaria', 'cities': ['Sofia', 'Plovdiv', 'Varna', 'Burgas', 'Ruse']},
            'HR': {'name': 'Croatia', 'cities': ['Zagreb', 'Split', 'Rijeka', 'Osijek', 'Zadar']},
            'CY': {'name': 'Cyprus', 'cities': ['Nicosia', 'Limassol', 'Larnaca', 'Paphos', 'Famagusta']},
            'CZ': {'name': 'Czechia', 'cities': ['Prague', 'Brno', 'Ostrava', 'Plzen', 'Liberec']},
            'DK': {'name': 'Denmark', 'cities': ['Copenhagen', 'Aarhus', 'Odense', 'Aalborg', 'Esbjerg']},
            'EE': {'name': 'Estonia', 'cities': ['Tallinn', 'Tartu', 'Narva', 'Parnu', 'Kohtla-Jarve']},
            'FI': {'name': 'Finland', 'cities': ['Helsinki', 'Espoo', 'Tampere', 'Vantaa', 'Oulu']},
            'FR': {'name': 'France', 'cities': ['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice']},
            'DE': {'name': 'Germany', 'cities': ['Berlin', 'Hamburg', 'Munich', 'Cologne', 'Frankfurt']},
            'GR': {'name': 'Greece', 'cities': ['Athens', 'Thessaloniki', 'Patras', 'Heraklion', 'Larissa']},
            'HU': {'name': 'Hungary', 'cities': ['Budapest', 'Debrecen', 'Szeged', 'Miskolc', 'Pécs']},
            'IE': {'name': 'Ireland', 'cities': ['Dublin', 'Cork', 'Galway', 'Waterford', 'Limerick']},
            'IT': {'name': 'Italy', 'cities': ['Rome', 'Milan', 'Naples', 'Turin', 'Palermo']},
            'LV': {'name': 'Latvia', 'cities': ['Riga', 'Daugavpils', 'Liepaja', 'Jelgava', 'Jurmala']},
            'LT': {'name': 'Lithuania', 'cities': ['Vilnius', 'Kaunas', 'Klaipeda', 'Siauliai', 'Panevezys']},
            'LU': {'name': 'Luxembourg', 'cities': ['Luxembourg City', 'Esch-sur-Alzette', 'Differdange', 'Dudelange']},
            'MT': {'name': 'Malta', 'cities': ['Valletta', 'Birkirkara', 'Mosta', 'Qormi', 'Zabbar']},
            'NL': {'name': 'Netherlands', 'cities': ['Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht', 'Eindhoven']},
            'PL': {'name': 'Poland', 'cities': ['Warsaw', 'Krakow', 'Lodz', 'Wroclaw', 'Poznan']},
            'PT': {'name': 'Portugal', 'cities': ['Lisbon', 'Porto', 'Vila Nova de Gaia', 'Amadora', 'Braga']},
            'RO': {'name': 'Romania', 'cities': ['Bucharest', 'Cluj-Napoca', 'Timisoara', 'Iasi', 'Constanta']},
            'SK': {'name': 'Slovakia', 'cities': ['Bratislava', 'Kosice', 'Presov', 'Zilina', 'Banska Bystrica']},
            'SI': {'name': 'Slovenia', 'cities': ['Ljubljana', 'Maribor', 'Celje', 'Kranj', 'Velenje']},
            'ES': {'name': 'Spain', 'cities': ['Madrid', 'Barcelona', 'Valencia', 'Seville', 'Zaragoza']},
            'SE': {'name': 'Sweden', 'cities': ['Stockholm', 'Gothenburg', 'Malmö', 'Uppsala', 'Västerås']}
        }
        
        # Business categories mapping
        self.categories_map = {
            'amenity=restaurant': 'Restaurant',
            'amenity=cafe': 'Café',
            'amenity=bar': 'Bar',
            'amenity=pub': 'Pub',
            'shop=supermarket': 'Supermarket',
            'shop=clothes': 'Clothing Store',
            'shop=bakery': 'Bakery',
            'shop=hairdresser': 'Hairdresser',
            'shop=pharmacy': 'Pharmacy',
            'amenity=hospital': 'Hospital',
            'amenity=bank': 'Bank',
            'amenity=hotel': 'Hotel',
            'tourism=hotel': 'Hotel',
            'office=company': 'Office',
            'craft=*': 'Services'
        }

    def get_city_bounds(self, city: str, country: str) -> Optional[Dict]:
        """Get geographical bounds for a city"""
        try:
            location = self.geolocator.geocode(f"{city}, {country}")
            if location:
                # Create a bounding box around the city (approximately 10km radius)
                lat, lon = location.latitude, location.longitude
                offset = 0.09  # Roughly 10km
                return {
                    'south': lat - offset,
                    'west': lon - offset,
                    'north': lat + offset,
                    'east': lon + offset
                }
        except Exception as e:
            print(f"Error getting bounds for {city}, {country}: {e}")
        return None

    def collect_from_openstreetmap(self, city: str, country_code: str, limit: int = 100) -> List[BusinessData]:
        """Collect business data from OpenStreetMap using Overpass API"""
        businesses = []
        country_name = self.eu_countries.get(country_code, {}).get('name', country_code)
        
        print(f"Collecting data for {city}, {country_name} from OpenStreetMap...")
        
        bounds = self.get_city_bounds(city, country_name)
        if not bounds:
            print(f"Could not find geographical bounds for {city}")
            return businesses
        
        # Overpass query to get various types of businesses
        query = f"""
        [out:json][timeout:30];
        (
          node["amenity"~"^(restaurant|cafe|bar|pub|hotel|hospital|bank|pharmacy)$"]({bounds['south']},{bounds['west']},{bounds['north']},{bounds['east']});
          node["shop"~"^(supermarket|clothes|bakery|hairdresser|pharmacy|convenience)$"]({bounds['south']},{bounds['west']},{bounds['north']},{bounds['east']});
          node["tourism"~"^(hotel|attraction|museum)$"]({bounds['south']},{bounds['west']},{bounds['north']},{bounds['east']});
          node["office"]({bounds['south']},{bounds['west']},{bounds['north']},{bounds['east']});
        );
        out center meta;
        """
        
        try:
            result = self.api.query(query)
            
            for node in result.nodes[:limit]:
                tags = node.tags
                
                # Extract business information
                name = tags.get('name', 'Unnamed Business')
                if not name or name == 'Unnamed Business':
                    continue
                
                # Determine category
                category = self._determine_category(tags)
                
                # Get address components
                address_parts = []
                if 'addr:street' in tags and 'addr:housenumber' in tags:
                    address_parts.append(f"{tags['addr:street']} {tags['addr:housenumber']}")
                elif 'addr:street' in tags:
                    address_parts.append(tags['addr:street'])
                
                address = ', '.join(address_parts) if address_parts else 'Address not available'
                
                # Create business data object
                business = BusinessData(
                    name=name,
                    category=category,
                    address=address,
                    city=city,
                    country=country_name,
                    country_code=country_code.lower(),
                    phone=tags.get('phone'),
                    website=tags.get('website'),
                    email=tags.get('email'),
                    latitude=float(node.lat),
                    longitude=float(node.lon),
                    description=tags.get('description'),
                    opening_hours=self._parse_opening_hours(tags.get('opening_hours')),
                    source="OpenStreetMap"
                )
                
                businesses.append(business)
                
        except Exception as e:
            print(f"Error collecting from OpenStreetMap: {e}")
        
        print(f"Collected {len(businesses)} businesses from OpenStreetMap")
        return businesses

    def _determine_category(self, tags: Dict) -> str:
        """Determine business category from OSM tags"""
        if 'amenity' in tags:
            amenity = tags['amenity']
            category_map = {
                'restaurant': 'Restaurant',
                'cafe': 'Café',
                'bar': 'Bar',
                'pub': 'Pub',
                'hotel': 'Hotel',
                'hospital': 'Hospital',
                'bank': 'Bank',
                'pharmacy': 'Pharmacy'
            }
            return category_map.get(amenity, 'Services')
        
        elif 'shop' in tags:
            shop = tags['shop']
            category_map = {
                'supermarket': 'Supermarket',
                'clothes': 'Clothing Store',
                'bakery': 'Bakery',
                'hairdresser': 'Hairdresser',
                'pharmacy': 'Pharmacy',
                'convenience': 'Convenience Store'
            }
            return category_map.get(shop, 'Retail')
        
        elif 'tourism' in tags:
            return 'Tourism'
        
        elif 'office' in tags:
            return 'Office'
        
        return 'Other'

    def _parse_opening_hours(self, hours_str: Optional[str]) -> Optional[Dict]:
        """Parse OpenStreetMap opening hours format"""
        if not hours_str:
            return None
        
        # This is a simplified parser - OSM opening hours can be very complex
        # For a production system, you'd want to use a proper library like "opening_hours"
        try:
            days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            hours_dict = {}
            
            # Simple cases like "Mo-Fr 09:00-18:00" or "24/7"
            if hours_str == "24/7":
                for day in days:
                    hours_dict[day] = "24 hours"
            elif "-" in hours_str and ":" in hours_str:
                # Extract time range
                parts = hours_str.split()
                if len(parts) >= 2:
                    time_range = parts[-1]  # Get the last part which should be the time
                    for day in days:
                        hours_dict[day] = time_range.replace('-', ' - ')
            
            return hours_dict if hours_dict else None
        except:
            return None

    def save_to_csv(self, businesses: List[BusinessData], filename: str):
        """Save collected business data to CSV file"""
        os.makedirs('data', exist_ok=True)
        filepath = os.path.join('data', filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            if businesses:
                fieldnames = list(asdict(businesses[0]).keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for business in businesses:
                    row = asdict(business)
                    # Convert opening_hours dict to JSON string for CSV
                    if row['opening_hours']:
                        row['opening_hours'] = json.dumps(row['opening_hours'])
                    writer.writerow(row)
        
        print(f"Saved {len(businesses)} businesses to {filepath}")

    def collect_all_eu_data(self, limit_per_city: int = 50):
        """Collect business data for all major EU cities"""
        all_businesses = []
        
        for country_code, country_info in self.eu_countries.items():
            print(f"\n=== Processing {country_info['name']} ({country_code}) ===")
            
            for city in country_info['cities'][:3]:  # Top 3 cities per country
                businesses = self.collect_from_openstreetmap(city, country_code, limit_per_city)
                all_businesses.extend(businesses)
                
                # Be respectful to the API
                time.sleep(2)
        
        # Save all collected data
        timestamp = int(time.time())
        self.save_to_csv(all_businesses, f'eu_businesses_{timestamp}.csv')
        
        print(f"\n=== COLLECTION COMPLETE ===")
        print(f"Total businesses collected: {len(all_businesses)}")
        
        # Print summary by country
        by_country = {}
        for business in all_businesses:
            if business.country not in by_country:
                by_country[business.country] = 0
            by_country[business.country] += 1
        
        print("\nBusinesses by country:")
        for country, count in sorted(by_country.items()):
            print(f"  {country}: {count}")

def main():
    parser = argparse.ArgumentParser(description='Collect EU business data from free sources')
    parser.add_argument('--country', type=str, help='Country code (e.g., AT, DE, FR)')
    parser.add_argument('--city', type=str, help='City name')
    parser.add_argument('--limit', type=int, default=100, help='Maximum number of businesses to collect')
    parser.add_argument('--all', action='store_true', help='Collect data for all EU countries')
    
    args = parser.parse_args()
    
    collector = EUBusinessCollector()
    
    if args.all:
        collector.collect_all_eu_data()
    elif args.country and args.city:
        businesses = collector.collect_from_openstreetmap(args.city, args.country.upper(), args.limit)
        timestamp = int(time.time())
        collector.save_to_csv(businesses, f'{args.city.lower()}_{args.country.lower()}_{timestamp}.csv')
    else:
        print("Please specify either --all flag or both --country and --city parameters")
        print("Example: python collect_business_data.py --country AT --city Vienna --limit 100")
        print("Or: python collect_business_data.py --all")

if __name__ == "__main__":
    main()