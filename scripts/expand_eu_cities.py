"""
Comprehensive EU Cities Importer - All 820+ Cities
Expands from 139 to 820+ cities across all 27 EU countries
"""

import os
import django
import requests
import json
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listacrosseu.settings')
django.setup()

from businesses.models import Country, City


class EUCitiesExpander:
    """Expand EU cities database to 820+ cities"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ListAcross.eu City Database Builder (contact@listacross.eu)'
        })
        self.added_cities = 0
        self.skipped_cities = 0
    
    def get_country_cities(self, country_code, country_name):
        """Get all cities for a specific country from GeoNames"""
        
        print(f"\n🏛️ Processing {country_name} ({country_code})...")
        
        try:
            # GeoNames API for cities with population > 5000
            url = "http://api.geonames.org/searchJSON"
            params = {
                'country': country_code,
                'featureClass': 'P',  # Populated places
                'maxRows': 1000,
                'username': 'demo',  # You should get your own GeoNames username
                'orderby': 'population'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('geonames', [])
            else:
                print(f"❌ API error for {country_name}: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error fetching cities for {country_name}: {e}")
            return []
    
    def add_cities_for_country(self, country):
        """Add cities for a specific country"""
        
        current_count = City.objects.filter(country=country).count()
        print(f"📊 Current cities in {country.name}: {current_count}")
        
        # Get cities from API
        cities_data = self.get_country_cities(country.code.lower(), country.name)
        
        for city_data in cities_data:
            city_name = city_data.get('name', '').strip()
            population = city_data.get('population', 0)
            lat = city_data.get('lat', 0)
            lng = city_data.get('lng', 0)
            
            # Skip if no name or very small population
            if not city_name or population < 1000:
                continue
            
            # Check if city already exists
            if City.objects.filter(name=city_name, country=country).exists():
                self.skipped_cities += 1
                continue
            
            try:
                # Create new city
                city = City.objects.create(
                    name=city_name,
                    country=country,
                    latitude=Decimal(str(lat)) if lat else None,
                    longitude=Decimal(str(lng)) if lng else None,
                    population=population,
                    is_capital=(city_name.lower() == self.get_capital_name(country.name).lower())
                )
                
                self.added_cities += 1
                print(f"✅ Added: {city_name} (pop: {population:,})")
                
            except Exception as e:
                print(f"❌ Error adding {city_name}: {e}")
    
    def get_capital_name(self, country_name):
        """Get capital city name for country"""
        capitals = {
            'Austria': 'Vienna',
            'Belgium': 'Brussels',
            'Bulgaria': 'Sofia',
            'Croatia': 'Zagreb',
            'Cyprus': 'Nicosia',
            'Czech Republic': 'Prague',
            'Denmark': 'Copenhagen',
            'Estonia': 'Tallinn',
            'Finland': 'Helsinki',
            'France': 'Paris',
            'Germany': 'Berlin',
            'Greece': 'Athens',
            'Hungary': 'Budapest',
            'Ireland': 'Dublin',
            'Italy': 'Rome',
            'Latvia': 'Riga',
            'Lithuania': 'Vilnius',
            'Luxembourg': 'Luxembourg',
            'Malta': 'Valletta',
            'Netherlands': 'Amsterdam',
            'Poland': 'Warsaw',
            'Portugal': 'Lisbon',
            'Romania': 'Bucharest',
            'Slovakia': 'Bratislava',
            'Slovenia': 'Ljubljana',
            'Spain': 'Madrid',
            'Sweden': 'Stockholm'
        }
        return capitals.get(country_name, '')
    
    def add_major_cities_manually(self):
        """Add major EU cities that might be missing"""
        
        major_cities = [
            # Germany - Major cities
            {'name': 'Munich', 'country': 'Germany', 'population': 1471508, 'lat': 48.1351, 'lng': 11.5820},
            {'name': 'Hamburg', 'country': 'Germany', 'population': 1899160, 'lat': 53.5511, 'lng': 9.9937},
            {'name': 'Cologne', 'country': 'Germany', 'population': 1085664, 'lat': 50.9375, 'lng': 6.9603},
            {'name': 'Frankfurt', 'country': 'Germany', 'population': 753056, 'lat': 50.1109, 'lng': 8.6821},
            
            # France - Major cities
            {'name': 'Marseille', 'country': 'France', 'population': 870018, 'lat': 43.2965, 'lng': 5.3698},
            {'name': 'Lyon', 'country': 'France', 'population': 515695, 'lat': 45.7640, 'lng': 4.8357},
            {'name': 'Nice', 'country': 'France', 'population': 342637, 'lat': 43.7102, 'lng': 7.2620},
            {'name': 'Toulouse', 'country': 'France', 'population': 479553, 'lat': 43.6047, 'lng': 1.4442},
            
            # Italy - Major cities
            {'name': 'Milan', 'country': 'Italy', 'population': 1378689, 'lat': 45.4642, 'lng': 9.1900},
            {'name': 'Naples', 'country': 'Italy', 'population': 967069, 'lat': 40.8518, 'lng': 14.2681},
            {'name': 'Turin', 'country': 'Italy', 'population': 870952, 'lat': 45.0703, 'lng': 7.6869},
            {'name': 'Florence', 'country': 'Italy', 'population': 382258, 'lat': 43.7696, 'lng': 11.2558},
            
            # Spain - Major cities
            {'name': 'Barcelona', 'country': 'Spain', 'population': 1620343, 'lat': 41.3851, 'lng': 2.1734},
            {'name': 'Valencia', 'country': 'Spain', 'population': 791413, 'lat': 39.4699, 'lng': -0.3763},
            {'name': 'Seville', 'country': 'Spain', 'population': 688711, 'lat': 37.3891, 'lng': -5.9845},
            {'name': 'Bilbao', 'country': 'Spain', 'population': 345821, 'lat': 43.2627, 'lng': -2.9253},
            
            # Netherlands - Major cities
            {'name': 'Rotterdam', 'country': 'Netherlands', 'population': 651446, 'lat': 51.9225, 'lng': 4.47917},
            {'name': 'The Hague', 'country': 'Netherlands', 'population': 548320, 'lat': 52.0705, 'lng': 4.3007},
            {'name': 'Utrecht', 'country': 'Netherlands', 'population': 357179, 'lat': 52.0907, 'lng': 5.1214},
            
            # Poland - Major cities
            {'name': 'Krakow', 'country': 'Poland', 'population': 779115, 'lat': 50.0647, 'lng': 19.9450},
            {'name': 'Gdansk', 'country': 'Poland', 'population': 470907, 'lat': 54.3520, 'lng': 18.6466},
            {'name': 'Wroclaw', 'country': 'Poland', 'population': 642492, 'lat': 51.1079, 'lng': 17.0385},
            
            # More major cities across EU...
        ]
        
        for city_data in major_cities:
            try:
                country = Country.objects.get(name=city_data['country'])
                
                if not City.objects.filter(name=city_data['name'], country=country).exists():
                    city = City.objects.create(
                        name=city_data['name'],
                        country=country,
                        latitude=Decimal(str(city_data['lat'])),
                        longitude=Decimal(str(city_data['lng'])),
                        population=city_data['population'],
                        is_capital=False
                    )
                    self.added_cities += 1
                    print(f"✅ Added major city: {city_data['name']}, {city_data['country']}")
                else:
                    self.skipped_cities += 1
                    
            except Exception as e:
                print(f"❌ Error adding {city_data['name']}: {e}")
    
    def run_expansion(self):
        """Run the full city expansion process"""
        
        print("🏛️ STARTING EU CITIES EXPANSION TO 820+ CITIES")
        print("=" * 60)
        
        initial_count = City.objects.count()
        print(f"📊 Starting with {initial_count} cities")
        
        # Add major cities first
        print("\n🏙️ PHASE 1: Adding Major EU Cities...")
        self.add_major_cities_manually()
        
        # Add cities for each country
        print("\n🌍 PHASE 2: Adding Cities by Country...")
        countries = Country.objects.all().order_by('name')
        
        for country in countries:
            try:
                self.add_cities_for_country(country)
            except Exception as e:
                print(f"❌ Error processing {country.name}: {e}")
        
        # Final statistics
        final_count = City.objects.count()
        
        print("\n" + "=" * 60)
        print("🎉 EU CITIES EXPANSION COMPLETED!")
        print(f"📊 Initial cities: {initial_count}")
        print(f"📊 Final cities: {final_count}")
        print(f"✅ Cities added: {self.added_cities}")
        print(f"⏭️ Cities skipped: {self.skipped_cities}")
        print(f"📈 Total increase: {final_count - initial_count}")
        
        # Show cities per country
        print("\n🏛️ CITIES PER COUNTRY:")
        for country in countries:
            count = City.objects.filter(country=country).count()
            print(f"  {country.name}: {count} cities")


if __name__ == "__main__":
    expander = EUCitiesExpander()
    expander.run_expansion()