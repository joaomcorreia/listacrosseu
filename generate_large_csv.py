"""
Generate a large CSV file for testing bulk import functionality
Creates realistic business data for European cities
"""
import csv
import random
from faker import Faker
import argparse

# Initialize Faker for different locales
fake_en = Faker('en_GB')  # English (UK)
fake_nl = Faker('nl_NL')  # Dutch
fake_fr = Faker('fr_FR')  # French
fake_de = Faker('de_DE')  # German

# European cities and countries
CITIES_DATA = [
    {'city': 'Amsterdam', 'country': 'Netherlands', 'postal_prefix': '10'},
    {'city': 'Berlin', 'country': 'Germany', 'postal_prefix': '10'},
    {'city': 'Paris', 'country': 'France', 'postal_prefix': '75'},
    {'city': 'Madrid', 'country': 'Spain', 'postal_prefix': '28'},
    {'city': 'Rome', 'country': 'Italy', 'postal_prefix': '00'},
    {'city': 'Vienna', 'country': 'Austria', 'postal_prefix': '10'},
    {'city': 'Brussels', 'country': 'Belgium', 'postal_prefix': '10'},
    {'city': 'Prague', 'country': 'Czech Republic', 'postal_prefix': '11'},
    {'city': 'Lisbon', 'country': 'Portugal', 'postal_prefix': '10'},
    {'city': 'Copenhagen', 'country': 'Denmark', 'postal_prefix': '15'},
]

# Business categories
CATEGORIES = [
    'Restaurant', 'Café', 'Bar', 'Hotel', 'Shop', 'Bakery', 'Pharmacy',
    'Bookstore', 'Clothing Store', 'Electronics Store', 'Grocery Store',
    'Hair Salon', 'Beauty Salon', 'Gym', 'Spa', 'Dentist', 'Doctor',
    'Law Office', 'Accounting Firm', 'Real Estate Agency', 'Travel Agency',
    'Car Rental', 'Taxi Service', 'Auto Repair', 'Bank', 'Insurance Agency',
    'Pet Store', 'Veterinarian', 'Florist', 'Garden Center', 'Hardware Store'
]

# Business name templates
BUSINESS_TEMPLATES = [
    "{name}'s {category}",
    "The {adjective} {category}",
    "{city} {category}",
    "{name} & {name2} {category}",
    "{category} {name}",
    "Central {category}",
    "Royal {category}",
    "Golden {category}",
    "Modern {category}",
    "Traditional {category}"
]

ADJECTIVES = [
    'Best', 'Premium', 'Quality', 'Fresh', 'Organic', 'Classic', 'Modern',
    'Traditional', 'Artisan', 'Boutique', 'Local', 'Family', 'Expert'
]

def generate_hours():
    """Generate realistic opening hours"""
    if random.random() < 0.1:  # 10% closed
        return "Closed"
    
    # Most businesses open between 7-10 AM
    open_hour = random.randint(7, 10)
    # Most close between 5-10 PM
    close_hour = random.randint(17, 22)
    
    return f"{open_hour:02d}:00-{close_hour:02d}:00"

def generate_business_data(num_records=6500):
    """Generate realistic business data"""
    businesses = []
    
    for i in range(num_records):
        # Choose random city and faker locale
        city_data = random.choice(CITIES_DATA)
        city = city_data['city']
        country = city_data['country']
        
        # Choose appropriate faker based on country
        if country in ['Netherlands', 'Belgium']:
            faker = fake_nl
        elif country == 'Germany':
            faker = fake_de
        elif country == 'France':
            faker = fake_fr
        else:
            faker = fake_en
        
        # Generate business name
        category = random.choice(CATEGORIES)
        template = random.choice(BUSINESS_TEMPLATES)
        
        name_parts = {
            'name': faker.last_name(),
            'name2': faker.last_name(),
            'category': category,
            'city': city,
            'adjective': random.choice(ADJECTIVES)
        }
        
        business_name = template.format(**name_parts)
        
        # Generate address
        address = faker.street_address()
        postal_code = f"{city_data['postal_prefix']}{random.randint(10, 99)} {faker.random_uppercase_letter()}{faker.random_uppercase_letter()}"
        
        # Generate contact info
        phone = faker.phone_number()
        email = f"info@{business_name.lower().replace(' ', '').replace("'", '')[:10]}.com"
        
        # Website (70% of businesses have one)
        website = ""
        if random.random() < 0.7:
            domain = business_name.lower().replace(' ', '').replace("'", '')[:15]
            website = f"https://www.{domain}.com"
        
        # Description
        descriptions = [
            f"Quality {category.lower()} in the heart of {city}",
            f"Traditional {category.lower()} serving the {city} community",
            f"Modern {category.lower()} with excellent service",
            f"Family-owned {category.lower()} since 1995",
            f"Premium {category.lower()} experience in {city}",
            f"Local {category.lower()} with friendly staff"
        ]
        description = random.choice(descriptions)
        
        # Opening hours (some businesses closed on certain days)
        hours = {
            'monday_hours': generate_hours(),
            'tuesday_hours': generate_hours(),
            'wednesday_hours': generate_hours(),
            'thursday_hours': generate_hours(),
            'friday_hours': generate_hours(),
            'saturday_hours': generate_hours() if random.random() < 0.8 else "Closed",
            'sunday_hours': generate_hours() if random.random() < 0.6 else "Closed",
        }
        
        # Coordinates (approximate for each city)
        city_coords = {
            'Amsterdam': (52.3676, 4.9041),
            'Berlin': (52.5200, 13.4050),
            'Paris': (48.8566, 2.3522),
            'Madrid': (40.4168, -3.7038),
            'Rome': (41.9028, 12.4964),
            'Vienna': (48.2082, 16.3738),
            'Brussels': (50.8503, 4.3517),
            'Prague': (50.0755, 14.4378),
            'Lisbon': (38.7223, -9.1393),
            'Copenhagen': (55.6761, 12.5683),
        }
        
        base_lat, base_lng = city_coords.get(city, (52.3676, 4.9041))
        # Add random offset within ~10km radius
        lat_offset = random.uniform(-0.05, 0.05)
        lng_offset = random.uniform(-0.05, 0.05)
        
        business = {
            'name': business_name,
            'description': description,
            'address': address,
            'phone_number': phone,
            'website': website,
            'email': email,
            'category': category,
            'city': city,
            'country': country,
            'postal_code': postal_code,
            'latitude': round(base_lat + lat_offset, 6),
            'longitude': round(base_lng + lng_offset, 6),
            'is_active': random.choice(['true', 'true', 'true', 'false']),  # 75% active
            'is_public': random.choice(['true', 'true', 'true', 'true', 'false']),  # 80% public
            'is_featured': random.choice(['true', 'false', 'false', 'false']),  # 25% featured
            **hours
        }
        
        businesses.append(business)
        
        # Progress indicator
        if (i + 1) % 1000 == 0:
            print(f"Generated {i + 1} businesses...")
    
    return businesses

def write_csv(businesses, filename):
    """Write businesses data to CSV file"""
    
    fieldnames = [
        'name', 'description', 'address', 'phone_number', 'website', 'email',
        'category', 'city', 'country', 'postal_code', 'latitude', 'longitude',
        'monday_hours', 'tuesday_hours', 'wednesday_hours', 'thursday_hours',
        'friday_hours', 'saturday_hours', 'sunday_hours',
        'is_active', 'is_public', 'is_featured'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for business in businesses:
            writer.writerow(business)
    
    print(f"\\nCSV file '{filename}' created with {len(businesses)} businesses")

def main():
    parser = argparse.ArgumentParser(description='Generate large CSV file for testing bulk import')
    parser.add_argument('--records', '-r', type=int, default=6500, 
                       help='Number of business records to generate (default: 6500)')
    parser.add_argument('--output', '-o', type=str, default='large_businesses.csv',
                       help='Output CSV filename (default: large_businesses.csv)')
    
    args = parser.parse_args()
    
    print(f"Generating {args.records} business records...")
    print(f"Output file: {args.output}")
    print("-" * 50)
    
    businesses = generate_business_data(args.records)
    write_csv(businesses, args.output)
    
    # File size info
    import os
    file_size = os.path.getsize(args.output)
    file_size_mb = file_size / (1024 * 1024)
    print(f"File size: {file_size_mb:.1f} MB")
    
    print("\\nSample data (first 3 records):")
    print("-" * 50)
    for i, business in enumerate(businesses[:3]):
        print(f"{i+1}. {business['name']} ({business['category']}) - {business['city']}, {business['country']}")

if __name__ == "__main__":
    main()