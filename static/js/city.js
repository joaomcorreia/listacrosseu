// City Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Get city and country from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const countryCode = urlParams.get('country') || 'at';
    const cityName = urlParams.get('city') || 'Vienna';
    
    // Load city data
    loadCityData(countryCode, cityName);
    
    // Initialize search
    initializeCitySearch(countryCode, cityName);
    
    // Load categories
    loadQuickCategories();
    
    // Load businesses
    loadCityBusinesses(countryCode, cityName);
    
    // Load nearby cities
    loadNearbyCities(countryCode, cityName);
    
    // Load city highlights
    loadCityHighlights(cityName);
});

function loadCityData(countryCode, cityName) {
    const cityData = {
        'Vienna': {
            country: 'Austria',
            population: '1.9M',
            totalBusinesses: 4521,
            avgRating: 4.6,
            description: 'Austria\'s elegant capital, Vienna combines imperial grandeur with modern innovation. Home to world-class museums, historic coffee houses, and a thriving business scene.'
        },
        'Paris': {
            country: 'France', 
            population: '2.2M',
            totalBusinesses: 25431,
            avgRating: 4.4,
            description: 'The City of Light offers unparalleled business opportunities in fashion, cuisine, technology, and culture. A global hub for luxury goods and innovation.'
        },
        'Berlin': {
            country: 'Germany',
            population: '3.7M', 
            totalBusinesses: 18765,
            avgRating: 4.5,
            description: 'Germany\'s dynamic capital is Europe\'s startup hub, combining rich history with cutting-edge technology and a vibrant creative scene.'
        },
        'Rome': {
            country: 'Italy',
            population: '2.9M',
            totalBusinesses: 12340,
            avgRating: 4.3,
            description: 'The Eternal City blends ancient history with modern commerce. A center for fashion, food, and cultural enterprises in the heart of Italy.'
        },
        'Madrid': {
            country: 'Spain',
            population: '3.3M',
            totalBusinesses: 15678,
            avgRating: 4.4,
            description: 'Spain\'s vibrant capital offers diverse business opportunities in finance, technology, and culture, with a lifestyle that balances work and leisure.'
        }
    };
    
    const data = cityData[cityName] || cityData['Vienna'];
    
    // Update page title and headers
    document.title = `${cityName}, ${data.country} - Business Directory | ListAcrossEU`;
    document.getElementById('city-title').textContent = cityName;
    document.getElementById('country-name').textContent = data.country;
    document.getElementById('city-population').textContent = data.population;
    document.getElementById('total-businesses').textContent = data.totalBusinesses.toLocaleString();
    document.getElementById('avg-rating').textContent = data.avgRating;
    document.getElementById('city-description').textContent = data.description;
    
    // Update other city name references
    document.getElementById('city-name-categories').textContent = cityName;
    document.getElementById('map-city-name').textContent = cityName;
    document.getElementById('city-name-highlights').textContent = cityName;
    document.getElementById('upgrade-city-name').textContent = cityName;
    document.getElementById('benefit-city-name').textContent = cityName;
}

function loadQuickCategories() {
    const categories = [
        { name: 'Restaurants', icon: '🍽', active: false },
        { name: 'Shopping', icon: '🛒', active: false },
        { name: 'Services', icon: '💼', active: false },
        { name: 'Healthcare', icon: '🏥', active: false },
        { name: 'Tourism', icon: '🏨', active: false },
        { name: 'Automotive', icon: '🚗', active: false },
        { name: 'Technology', icon: '💻', active: false }
    ];
    
    const container = document.getElementById('categories-container');
    
    container.innerHTML = categories.map(category => `
        <div class="category-chip" onclick="filterByCategory('${category.name.toLowerCase()}')"
             data-category="${category.name.toLowerCase()}">
            ${category.icon} ${category.name}
        </div>
    `).join('');
}

function loadCityBusinesses(countryCode, cityName) {
    // Demo businesses for the city
    const businesses = [
        {
            id: 1,
            name: 'Café Central Vienna',
            category: 'Restaurant',
            address: 'Herrengasse 14, 1010 Vienna',
            phone: '+43 1 533 3763',
            rating: 4.5,
            reviewCount: 1247,
            hours: 'Open until 10:00 PM',
            description: 'Historic Viennese coffeehouse serving traditional Austrian cuisine and world-famous coffee since 1876.'
        },
        {
            id: 2,
            name: 'Vienna Tech Solutions',
            category: 'Technology',
            address: 'Mariahilfer Strasse 88, 1070 Vienna',
            phone: '+43 1 234 5678',
            rating: 4.3,
            reviewCount: 89,
            hours: 'Open until 6:00 PM',
            description: 'Leading IT consulting firm specializing in digital transformation and software development.'
        },
        {
            id: 3,
            name: 'Naschmarkt Deli',
            category: 'Food & Retail',
            address: 'Naschmarkt 15, 1060 Vienna',
            phone: '+43 1 987 6543',
            rating: 4.7,
            reviewCount: 321,
            hours: 'Open until 7:00 PM',
            description: 'Gourmet delicatessen offering finest Austrian and international specialties.'
        },
        {
            id: 4,
            name: 'Wellness Spa Vienna',
            category: 'Healthcare',
            address: 'Graben 21, 1010 Vienna',
            phone: '+43 1 555 0123',
            rating: 4.8,
            reviewCount: 156,
            hours: 'Open until 9:00 PM',
            description: 'Luxury wellness center offering premium spa treatments and health services.'
        },
        {
            id: 5,
            name: 'Fashion Boutique Wien',
            category: 'Retail',
            address: 'Kärntner Strasse 32, 1010 Vienna',
            phone: '+43 1 777 8899',
            rating: 4.4,
            reviewCount: 203,
            hours: 'Open until 8:00 PM',
            description: 'Exclusive fashion boutique featuring Austrian designers and international luxury brands.'
        },
        {
            id: 6,
            name: 'Hotel Sacher Vienna',
            category: 'Tourism',
            address: 'Philharmoniker Strasse 4, 1010 Vienna',
            phone: '+43 1 514 560',
            rating: 4.9,
            reviewCount: 892,
            hours: '24 hours',
            description: 'Legendary luxury hotel in the heart of Vienna, famous for the original Sachertorte.'
        }
    ];
    
    const container = document.getElementById('businesses-list');
    
    container.innerHTML = businesses.map(business => `
        <div class="business-item" onclick="window.location.href='business-listing.html?id=${business.id}'">
            <div class="business-header">
                <h3 class="business-name">${business.name}</h3>
                <span class="business-category">${business.category}</span>
            </div>
            <div class="business-details">
                <div class="business-location">📍 ${business.address}</div>
                <div class="business-phone">📞 ${business.phone}</div>
                <div class="business-hours">🕐 ${business.hours}</div>
            </div>
            <div class="business-rating">
                <span class="stars">${'★'.repeat(Math.floor(business.rating))}${'☆'.repeat(5-Math.floor(business.rating))}</span>
                <span>${business.rating} (${business.reviewCount} reviews)</span>
            </div>
            <p class="business-description">${business.description}</p>
        </div>
    `).join('');
}

function loadNearbyCities(countryCode, cityName) {
    const nearbyCities = {
        'Vienna': ['Bratislava, Slovakia', 'Brno, Czechia', 'Graz, Austria', 'Salzburg, Austria'],
        'Paris': ['Brussels, Belgium', 'London, UK', 'Amsterdam, Netherlands', 'Lyon, France'],
        'Berlin': ['Hamburg, Germany', 'Prague, Czechia', 'Warsaw, Poland', 'Munich, Germany'],
        'Rome': ['Naples, Italy', 'Florence, Italy', 'Milan, Italy', 'Bologna, Italy'],
        'Madrid': ['Barcelona, Spain', 'Lisbon, Portugal', 'Valencia, Spain', 'Seville, Spain']
    };
    
    const cities = nearbyCities[cityName] || nearbyCities['Vienna'];
    const container = document.getElementById('nearby-cities-list');
    
    container.innerHTML = cities.map(city => `
        <div class="nearby-city" onclick="searchNearbyCity('${city}')">
            ${city}
        </div>
    `).join('');
}

function loadCityHighlights(cityName) {
    const highlights = {
        'Vienna': [
            { icon: '🎼', title: 'Cultural Heritage', description: 'UNESCO World Heritage historic center' },
            { icon: '☕', title: 'Coffee Culture', description: 'Traditional Viennese coffee houses' },
            { icon: '🏛', title: 'Imperial Architecture', description: 'Stunning palaces and museums' },
            { icon: '🎭', title: 'Arts Scene', description: 'World-class opera and theaters' }
        ],
        'Paris': [
            { icon: '🗼', title: 'Iconic Landmarks', description: 'Eiffel Tower and Notre-Dame' },
            { icon: '🍷', title: 'Culinary Excellence', description: 'World\'s finest restaurants' },
            { icon: '👗', title: 'Fashion Capital', description: 'Global fashion and luxury hub' },
            { icon: '🎨', title: 'Art & Culture', description: 'Louvre and countless galleries' }
        ],
        'Berlin': [
            { icon: '🚀', title: 'Startup Hub', description: 'Europe\'s leading tech ecosystem' },
            { icon: '🧱', title: 'Historical Significance', description: 'Rich 20th century history' },
            { icon: '🎵', title: 'Music Scene', description: 'Vibrant nightlife and clubs' },
            { icon: '🌍', title: 'International City', description: 'Diverse and cosmopolitan' }
        ],
        'Rome': [
            { icon: '🏛', title: 'Ancient History', description: 'Colosseum and Roman Forum' },
            { icon: '🍝', title: 'Authentic Cuisine', description: 'Traditional Italian flavors' },
            { icon: '⛪', title: 'Vatican City', description: 'St. Peter\'s and Sistine Chapel' },
            { icon: '🎬', title: 'Cinema History', description: 'Cinecittà film studios' }
        ],
        'Madrid': [
            { icon: '🏛', title: 'Royal Heritage', description: 'Royal Palace and gardens' },
            { icon: '🎨', title: 'Art Triangle', description: 'Prado, Reina Sofia, Thyssen' },
            { icon: '🌅', title: 'Vibrant Lifestyle', description: 'Late-night dining culture' },
            { icon: '⚽', title: 'Football Culture', description: 'Real Madrid and Atletico' }
        ]
    };
    
    const cityHighlights = highlights[cityName] || highlights['Vienna'];
    const container = document.getElementById('highlights-container');
    
    container.innerHTML = cityHighlights.map(highlight => `
        <div class="highlight-card">
            <span class="highlight-icon">${highlight.icon}</span>
            <h4 class="highlight-title">${highlight.title}</h4>
            <p class="highlight-description">${highlight.description}</p>
        </div>
    `).join('');
}

function initializeCitySearch(countryCode, cityName) {
    const searchInput = document.getElementById('local-search-input');
    const searchBtn = document.getElementById('local-search-btn');
    
    const performSearch = () => {
        const query = searchInput.value.trim();
        const category = document.getElementById('category-filter').value;
        const distance = document.getElementById('distance-filter').value;
        
        if (!query && !category) {
            alert('Please enter a search term or select a category');
            return;
        }
        
        // Build search URL
        const params = new URLSearchParams();
        if (query) params.append('q', query);
        if (category) params.append('category', category);
        if (distance) params.append('distance', distance);
        params.append('city', cityName);
        params.append('country', countryCode);
        
        window.location.href = `search-results.html?${params.toString()}`;
    };
    
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performSearch();
    });
}

// Utility Functions
function showMap() {
    alert('Interactive map integration coming soon!');
}

function scrollToSearch() {
    document.querySelector('.search-section').scrollIntoView({ behavior: 'smooth' });
}

function filterByCategory(category) {
    // Update active state
    document.querySelectorAll('.category-chip').forEach(chip => {
        chip.classList.remove('active');
        if (chip.dataset.category === category) {
            chip.classList.add('active');
        }
    });
    
    // Filter businesses (in a real app, this would filter the actual results)
    console.log(`Filtering by category: ${category}`);
}

function searchNearbyCity(cityName) {
    const [city, country] = cityName.split(', ');
    const countryCode = getCountryCodeByName(country);
    
    if (countryCode) {
        window.location.href = `city.html?country=${countryCode}&city=${encodeURIComponent(city)}`;
    }
}

function getCountryName(code) {
    const countryNames = {
        'at': 'Austria', 'be': 'Belgium', 'bg': 'Bulgaria', 'hr': 'Croatia',
        'cy': 'Cyprus', 'cz': 'Czechia', 'dk': 'Denmark', 'ee': 'Estonia',
        'fi': 'Finland', 'fr': 'France', 'de': 'Germany', 'gr': 'Greece',
        'hu': 'Hungary', 'ie': 'Ireland', 'it': 'Italy', 'lv': 'Latvia',
        'lt': 'Lithuania', 'lu': 'Luxembourg', 'mt': 'Malta', 'nl': 'Netherlands',
        'pl': 'Poland', 'pt': 'Portugal', 'ro': 'Romania', 'sk': 'Slovakia',
        'si': 'Slovenia', 'es': 'Spain', 'se': 'Sweden'
    };
    return countryNames[code] || 'Austria';
}

function getCountryCodeByName(countryName) {
    const countryCodes = {
        'Austria': 'at', 'Belgium': 'be', 'Bulgaria': 'bg', 'Croatia': 'hr',
        'Cyprus': 'cy', 'Czechia': 'cz', 'Denmark': 'dk', 'Estonia': 'ee',
        'Finland': 'fi', 'France': 'fr', 'Germany': 'de', 'Greece': 'gr',
        'Hungary': 'hu', 'Ireland': 'ie', 'Italy': 'it', 'Latvia': 'lv',
        'Lithuania': 'lt', 'Luxembourg': 'lu', 'Malta': 'mt', 'Netherlands': 'nl',
        'Poland': 'pl', 'Portugal': 'pt', 'Romania': 'ro', 'Slovakia': 'sk',
        'Slovenia': 'si', 'Spain': 'es', 'Sweden': 'se', 'UK': 'gb'
    };
    return countryCodes[countryName];
}