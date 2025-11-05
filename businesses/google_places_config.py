# Google Places API Configuration
import os

# To get started:
# 1. Go to Google Cloud Console: https://console.cloud.google.com/
# 2. Create a new project or select existing
# 3. Enable the Places API (New)
# 4. Create an API key with Places API permissions
# 5. Add your API key to .env file as GOOGLE_PLACES_API_KEY=your_key_here

# SECURITY: Never commit real API keys! Use environment variables instead.
GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY', 'AIzaSyBmKk3uM1BZV_qTuodk9fQmYWLzp1J-k48')

# Example (DON'T use this fake key):
# GOOGLE_PLACES_API_KEY = "AIzaSyC4YT8s-lxmKp9X2b1Fg7Hj8Kl3Mn5Qr9S"

# API Endpoints
GOOGLE_PLACES_SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"
GOOGLE_PLACES_DETAILS_URL = "https://places.googleapis.com/v1/places/{place_id}"

# Request limits (to avoid hitting quotas)
MAX_RESULTS_PER_SEARCH = 20  # Max per API call
DAILY_API_LIMIT = 1000       # Adjust based on your quota
SEARCHES_PER_CITY = 5        # Number of different search queries per city

# Business categories to search for
SEARCH_CATEGORIES = [
    # Restaurants
    "restaurant", "pizza", "italian restaurant", "french restaurant", 
    "chinese restaurant", "cafe", "bar", "fast food", "bakery",
    
    # Hotels & Accommodation  
    "hotel", "bed and breakfast", "hostel", "vacation rental",
    
    # Shopping
    "supermarket", "pharmacy", "clothing store", "shoe store", 
    "electronics store", "bookstore", "jewelry store",
    
    # Services
    "bank", "gas station", "auto repair", "hair salon", "dentist",
    "lawyer", "accountant", "real estate office", "insurance agency",
    
    # Health & Beauty
    "doctor", "physiotherapy", "veterinarian", "spa", "gym",
    
    # Education & Culture
    "school", "library", "museum", "art gallery", "music store",
    
    # Entertainment
    "cinema", "bowling alley", "casino", "night club",
    
    # Automotive
    "car dealer", "tire shop", "car wash", "motorcycle dealer",
    
    # Professional Services
    "marketing agency", "web design", "consultant", "architect"
]

# City search priorities (UPDATED FOR NETHERLANDS, PORTUGAL, BELGIUM FOCUS)
PRIORITY_CITIES = [
    # Netherlands - Priority targets
    "Amsterdam, Netherlands", "Rotterdam, Netherlands", "The Hague, Netherlands",
    "Utrecht, Netherlands", "Eindhoven, Netherlands", "Tilburg, Netherlands",
    "Groningen, Netherlands", "Almere, Netherlands",
    
    # Portugal - Priority targets  
    "Lisbon, Portugal", "Porto, Portugal", "Braga, Portugal", "Coimbra, Portugal",
    "Funchal, Portugal", "Aveiro, Portugal", "Faro, Portugal", "Cascais, Portugal",
    "Amadora, Portugal", "Almada, Portugal",
    
    # Belgium - Priority targets
    "Brussels, Belgium", "Antwerp, Belgium", "Ghent, Belgium", "Charleroi, Belgium",
    "Liège, Belgium", "Bruges, Belgium",
    
    # Existing successful cities (keep for comparison)
    "Berlin, Germany", "Munich, Germany", "Hamburg, Germany", "Cologne, Germany",
    "Madrid, Spain", "Barcelona, Spain", "Valencia, Spain", "Seville, Spain",
    "Paris, France", "Lyon, France", "Marseille, France", "Toulouse, France",
    "Vienna, Austria", "Graz, Austria", "Salzburg, Austria",
    "Warsaw, Poland", "Krakow, Poland", "Gdansk, Poland",
    "Budapest, Hungary", "Debrecen, Hungary",
    "Stockholm, Sweden", "Gothenburg, Sweden", "Malmö, Sweden",
    "Helsinki, Finland", "Espoo, Finland", "Tampere, Finland",
    "Dublin, Ireland", "Cork, Ireland",
    "Prague, Czech Republic", "Brno, Czech Republic",
    "Lisbon, Portugal", "Porto, Portugal", "Braga, Portugal",
    "Athens, Greece", "Thessaloniki, Greece",
    "Zagreb, Croatia", "Split, Croatia",
    "Ljubljana, Slovenia", "Maribor, Slovenia",
    "Copenhagen, Denmark", "Aarhus, Denmark",
    "Sofia, Bulgaria", "Plovdiv, Bulgaria",
    "Bucharest, Romania", "Cluj-Napoca, Romania",
    "Tallinn, Estonia", "Tartu, Estonia",
    "Riga, Latvia", "Daugavpils, Latvia",
    "Vilnius, Lithuania", "Kaunas, Lithuania",
    "Valletta, Malta", "Birkirkara, Malta",
    "Nicosia, Cyprus", "Limassol, Cyprus",
    "Luxembourg City, Luxembourg", "Esch-sur-Alzette, Luxembourg",
    "Bratislava, Slovakia", "Košice, Slovakia"
]