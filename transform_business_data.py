"""
Transform real business data CSV to match our Django Business model
Maps fields from your exported data to our database schema
"""
import csv
import os
import uuid
from datetime import datetime
import re

def clean_name(name):
    """Clean business names"""
    if not name or name == '-':
        return None
    # Remove special characters at the start
    name = re.sub(r'^[#&+\-\s]+', '', name)
    return name.strip() if name.strip() else None

def clean_phone(phone):
    """Clean phone numbers"""
    if not phone or phone == '-':
        return ''
    # Remove spaces and format consistently
    return re.sub(r'\s+', ' ', phone.strip())

def clean_website(website):
    """Clean website URLs"""
    if not website or website == '-' or 'example.com' in website.lower():
        return ''
    if not website.startswith(('http://', 'https://')):
        website = 'https://' + website
    return website

def clean_email(email):
    """Clean email addresses"""
    if not email or email == '-' or '@.com' in email or 'info@' in email and len(email.split('@')[0]) < 4:
        return ''
    return email.lower().strip()

def map_category(category_name):
    """Map category names to standardized categories"""
    category_mapping = {
        'Law Firms': 'Legal Services',
        'Fashion Boutiques': 'Clothing Store',
        'Veterinary Clinics': 'Veterinary',
        'Banks': 'Bank',
        'Restaurants': 'Restaurant',
        'Cafés': 'Café',
        'Hotels': 'Hotel',
        'Shops': 'Shop',
        'Bakeries': 'Bakery',
        'Pharmacies': 'Pharmacy',
        'Bookstores': 'Bookstore',
        'Beauty Salons': 'Beauty Salon',
        'Hair Salons': 'Hair Salon',
        'Fitness Centers': 'Gym',
        'Medical Clinics': 'Doctor',
        'Dental Clinics': 'Dentist',
    }
    
    return category_mapping.get(category_name, category_name)

def clean_hours(hours_str):
    """Clean opening hours format"""
    if not hours_str or hours_str.strip() == '':
        return ''
    hours_str = hours_str.strip()
    if hours_str.lower() in ['closed', 'fermé', 'cerrado', 'chiuso', 'gesloten']:
        return 'Closed'
    return hours_str

def transform_csv_data(input_file, output_file):
    """Transform the exported CSV to match our Django model"""
    
    print(f"Transforming {input_file} to {output_file}...")
    
    # Our target CSV headers (matching Django Business model)
    output_headers = [
        'name', 'description', 'address', 'phone_number', 'website', 'email',
        'category', 'city', 'country', 'postal_code', 'latitude', 'longitude',
        'monday_hours', 'tuesday_hours', 'wednesday_hours', 'thursday_hours',
        'friday_hours', 'saturday_hours', 'sunday_hours',
        'is_active', 'is_public', 'is_featured'
    ]
    
    transformed_count = 0
    skipped_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=output_headers)
        writer.writeheader()
        
        for row_num, row in enumerate(reader, start=2):  # Start at 2 because header is row 1
            try:
                # Clean and map the data
                business_name = clean_name(row.get('name', ''))
                
                # Skip rows with invalid names
                if not business_name:
                    print(f"Row {row_num}: Skipping - no valid business name")
                    skipped_count += 1
                    continue
                
                # Map the fields
                transformed_row = {
                    'name': business_name,
                    'description': (row.get('description', '') or row.get('short_description', '')).strip(),
                    'address': row.get('address', '').strip(),
                    'phone_number': clean_phone(row.get('phone', '')),
                    'website': clean_website(row.get('website', '')),
                    'email': clean_email(row.get('email', '')),
                    'category': map_category(row.get('category_name', 'Other')),
                    'city': row.get('city_name', '').strip(),
                    'country': row.get('country_name', '').strip(),
                    'postal_code': row.get('postal_code', '').strip(),
                    'latitude': row.get('latitude', '').strip(),
                    'longitude': row.get('longitude', '').strip(),
                    'monday_hours': clean_hours(row.get('monday_hours', '')),
                    'tuesday_hours': clean_hours(row.get('tuesday_hours', '')),
                    'wednesday_hours': clean_hours(row.get('wednesday_hours', '')),
                    'thursday_hours': clean_hours(row.get('thursday_hours', '')),
                    'friday_hours': clean_hours(row.get('friday_hours', '')),
                    'saturday_hours': clean_hours(row.get('saturday_hours', '')),
                    'sunday_hours': clean_hours(row.get('sunday_hours', '')),
                    'is_active': 'true',  # Assume all imported businesses are active
                    'is_public': 'true',  # Make all imported businesses public
                    'is_featured': row.get('featured', 'false').lower()
                }
                
                writer.writerow(transformed_row)
                transformed_count += 1
                
                # Progress indicator
                if transformed_count % 500 == 0:
                    print(f"Processed {transformed_count} businesses...")
                    
            except Exception as e:
                print(f"Row {row_num}: Error processing - {str(e)}")
                skipped_count += 1
                continue
    
    print(f"\\nTransformation complete!")
    print(f"✅ Successfully transformed: {transformed_count} businesses")
    print(f"⚠️  Skipped rows: {skipped_count}")
    print(f"📁 Output file: {output_file}")
    
    # File size info
    file_size = os.path.getsize(output_file)
    file_size_mb = file_size / (1024 * 1024)
    print(f"📊 File size: {file_size_mb:.1f} MB")
    
    return transformed_count, skipped_count

if __name__ == "__main__":
    input_file = "real_businesses_data.csv"
    output_file = "cleaned_businesses_for_import.csv"
    
    if os.path.exists(input_file):
        transform_csv_data(input_file, output_file)
    else:
        print(f"❌ Input file {input_file} not found!")
        print("Please make sure the file is in the current directory.")