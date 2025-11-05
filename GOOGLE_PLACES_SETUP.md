# Google Places API Integration Setup

## 1. Set Your API Key

You have several options to provide your Google Places API key:

### Option A: Environment Variable (Recommended)
```cmd
set GOOGLE_PLACES_API_KEY=AIzaSyBmKk3uM1BZV_qTuodk9fQmYWLzp1J-k48
```

### Option B: Command Line Argument
```cmd
python manage.py import_google_places --AIzaSyBmKk3uM1BZV_qTuodk9fQmYWLzp1J-k48 --query "restaurants in Paris"
```

## 2. Usage Examples

### Search by Query
```cmd
# Basic query search
python manage.py import_google_places --query "restaurants in Paris"

# Query with location bias
python manage.py import_google_places --query "cafes" --location "Barcelona, Spain" --region "es"

# Assign to specific user
python manage.py import_google_places --query "hotels in Amsterdam" --user your_username
```

### Search Nearby Places
```cmd
# Nearby search without type filter
python manage.py import_google_places --nearby "Lyon, France"

# Nearby search with type filter
python manage.py import_google_places --nearby "Madrid, Spain" --type restaurant

# Nearby search for specific business types
python manage.py import_google_places --nearby "Berlin, Germany" --type store
```

## 3. Available Place Types

Common Google Places types you can use with --type:
- `restaurant` - Restaurants and eateries
- `cafe` - Coffee shops and cafes
- `store` - General retail stores
- `lodging` - Hotels and accommodation
- `tourist_attraction` - Tourist attractions
- `shopping_mall` - Shopping centers
- `pharmacy` - Pharmacies
- `hospital` - Healthcare facilities
- `gym` - Fitness centers
- `beauty_salon` - Beauty and wellness
- `car_dealer` - Automotive businesses
- `bank` - Financial services
- `real_estate_agency` - Real estate
- `lawyer` - Legal services
- `school` - Educational institutions

## 4. Import Process

The import system will:

1. **Search Google Places** using your query or location
2. **Get detailed information** for each place found
3. **Check for duplicates** using Google Place ID
4. **Map business types** to your existing categories
5. **Create new categories** if needed
6. **Save to database** with proper formatting
7. **Track import progress** with real-time updates

## 5. Data Mapping

Google Places data is mapped to your Business model:
- **Name** → Business name
- **Address** → Parsed into address, city, country
- **Phone** → Business phone number
- **Website** → Business website
- **Coordinates** → Latitude/longitude
- **Opening Hours** → Mapped to weekday hour fields
- **Types** → Converted to appropriate categories
- **Rating** → Stored in description for now

## 6. Rate Limiting

The system includes built-in rate limiting:
- **0.1 seconds** between API calls (configurable)
- **Respects Google's quotas** and limits
- **Automatic retry** for temporary failures

## 7. Progress Tracking

Monitor import progress:
- Real-time progress updates
- Success/skip/error counts
- Detailed logging to console and files
- Cached progress data for web interface

## 8. Next Steps

After setting your API key, try a small test import:

```cmd
set GOOGLE_PLACES_API_KEY=AIzaSyBmKk3uM1BZV_qTuodk9fQmYWLzp1J-k48
python manage.py import_google_places --query "cafes in Paris" --region "fr"
```

This will search for cafes in Paris and import them to your database!