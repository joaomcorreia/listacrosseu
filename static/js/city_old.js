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
            totalBusinesses: 15432,
            avgRating: 4.7,
            description: 'The Eternal City blends ancient heritage with modern commerce, offering unique opportunities in tourism, fashion, and traditional craftsmanship.'
        },
        'Madrid': {
            country: 'Spain',
            population: '3.3M',
            totalBusinesses: 16789,
            avgRating: 4.5,
            description: 'Spain\'s vibrant capital is a major business center offering opportunities across finance, technology, tourism, and cultural industries.'
        }
    };
    
    const data = cityData[cityName] || cityData['Vienna'];
    const countryName = getCountryName(countryCode);
    
    // Update page content
    updateCityContent(data, cityName, countryName, countryCode);
}

function updateCityContent(data, cityName, countryName, countryCode) {
    // Update title and meta
    document.title = `${cityName}, ${countryName} - Business Directory | ListAcross EU`;
    
    // Update city header
    document.getElementById('city-title').textContent = `Businesses in ${cityName}, ${countryName}`;
    document.getElementById('total-businesses').textContent = data.totalBusinesses.toLocaleString();
    document.getElementById('avg-rating').textContent = data.avgRating;
    document.getElementById('city-population').textContent = data.population;
    document.getElementById('city-description').textContent = data.description;
    
    // Update breadcrumb
    document.getElementById('country-link').textContent = countryName;
    document.getElementById('country-link').href = `country.html?code=${countryCode}&name=${encodeURIComponent(countryName)}`;
    document.getElementById('city-name').textContent = cityName;
    
    // Update other city name references
    document.getElementById('city-name-categories').textContent = cityName;
    document.getElementById('map-city-name').textContent = cityName;
    document.getElementById('city-name-highlights').textContent = cityName;
    document.getElementById('upgrade-city-name').textContent = cityName;
    document.getElementById('benefit-city-name').textContent = cityName;
}\n\nfunction loadQuickCategories() {\n    const categories = [\n        { name: 'Restaurants', icon: '🍽️', active: false },\n        { name: 'Shopping', icon: '🛍️', active: false },\n        { name: 'Services', icon: '💼', active: false },\n        { name: 'Healthcare', icon: '🏥', active: false },\n        { name: 'Tourism', icon: '🏨', active: false },\n        { name: 'Automotive', icon: '🚗', active: false },\n        { name: 'Technology', icon: '💻', active: false }\n    ];\n    \n    const container = document.getElementById('categories-container');\n    \n    container.innerHTML = categories.map(category => `\n        <div class=\"category-chip\" onclick=\"filterByCategory('${category.name.toLowerCase()}')\"\n             data-category=\"${category.name.toLowerCase()}\">\n            ${category.icon} ${category.name}\n        </div>\n    `).join('');\n}\n\nfunction loadCityBusinesses(countryCode, cityName) {\n    // Demo businesses for the city\n    const businesses = [\n        {\n            id: 1,\n            name: 'Café Central Vienna',\n            category: 'Restaurant',\n            address: 'Herrengasse 14, 1010 Vienna',\n            phone: '+43 1 533 3763',\n            rating: 4.5,\n            reviewCount: 1247,\n            hours: 'Open until 10:00 PM',\n            description: 'Historic Viennese coffeehouse serving traditional Austrian cuisine and world-famous coffee since 1876.'\n        },\n        {\n            id: 2,\n            name: 'Vienna Tech Solutions',\n            category: 'Technology',\n            address: 'Mariahilfer Strasse 88, 1070 Vienna',\n            phone: '+43 1 234 5678',\n            rating: 4.3,\n            reviewCount: 89,\n            hours: 'Open until 6:00 PM',\n            description: 'Leading IT consulting firm specializing in digital transformation and software development.'\n        },\n        {\n            id: 3,\n            name: 'Naschmarkt Deli',\n            category: 'Food & Retail',\n            address: 'Naschmarkt 15, 1060 Vienna',\n            phone: '+43 1 987 6543',\n            rating: 4.7,\n            reviewCount: 321,\n            hours: 'Open until 7:00 PM',\n            description: 'Gourmet delicatessen offering finest Austrian and international specialties.'\n        },\n        {\n            id: 4,\n            name: 'Wellness Spa Vienna',\n            category: 'Healthcare',\n            address: 'Graben 21, 1010 Vienna',\n            phone: '+43 1 555 0123',\n            rating: 4.8,\n            reviewCount: 156,\n            hours: 'Open until 9:00 PM',\n            description: 'Luxury wellness center offering premium spa treatments and health services.'\n        },\n        {\n            id: 5,\n            name: 'Fashion Boutique Wien',\n            category: 'Retail',\n            address: 'Kärntner Strasse 32, 1010 Vienna',\n            phone: '+43 1 777 8899',\n            rating: 4.4,\n            reviewCount: 203,\n            hours: 'Open until 8:00 PM',\n            description: 'Exclusive fashion boutique featuring Austrian designers and international luxury brands.'\n        },\n        {\n            id: 6,\n            name: 'Hotel Sacher Vienna',\n            category: 'Tourism',\n            address: 'Philharmoniker Strasse 4, 1010 Vienna',\n            phone: '+43 1 514 560',\n            rating: 4.9,\n            reviewCount: 892,\n            hours: '24 hours',\n            description: 'Legendary luxury hotel in the heart of Vienna, famous for the original Sachertorte.'\n        }\n    ];\n    \n    const container = document.getElementById('businesses-list');\n    \n    container.innerHTML = businesses.map(business => `\n        <div class=\"business-item\" onclick=\"window.location.href='business-listing.html?id=${business.id}'\">\n            <div class=\"business-header\">\n                <h3 class=\"business-name\">${business.name}</h3>\n                <span class=\"business-category\">${business.category}</span>\n            </div>\n            <div class=\"business-details\">\n                <div class=\"business-location\">📍 ${business.address}</div>\n                <div class=\"business-phone\">📞 ${business.phone}</div>\n                <div class=\"business-hours\">🕐 ${business.hours}</div>\n            </div>\n            <div class=\"business-rating\">\n                <span class=\"stars\">${'★'.repeat(Math.floor(business.rating))}${'☆'.repeat(5-Math.floor(business.rating))}</span>\n                <span>${business.rating} (${business.reviewCount} reviews)</span>\n            </div>\n            <p class=\"business-description\">${business.description}</p>\n        </div>\n    `).join('');\n}\n\nfunction loadNearbyCities(countryCode, cityName) {\n    const nearbyCities = {\n        'Vienna': ['Bratislava, Slovakia', 'Brno, Czechia', 'Graz, Austria', 'Salzburg, Austria'],\n        'Paris': ['Brussels, Belgium', 'London, UK', 'Amsterdam, Netherlands', 'Lyon, France'],\n        'Berlin': ['Hamburg, Germany', 'Prague, Czechia', 'Warsaw, Poland', 'Munich, Germany'],\n        'Rome': ['Naples, Italy', 'Florence, Italy', 'Milan, Italy', 'Bologna, Italy'],\n        'Madrid': ['Barcelona, Spain', 'Lisbon, Portugal', 'Valencia, Spain', 'Seville, Spain']\n    };\n    \n    const cities = nearbyCities[cityName] || nearbyCities['Vienna'];\n    const container = document.getElementById('nearby-cities-list');\n    \n    container.innerHTML = cities.map(city => `\n        <div class=\"nearby-city\" onclick=\"searchNearbyCity('${city}')\">\n            ${city}\n        </div>\n    `).join('');\n}\n\nfunction loadCityHighlights(cityName) {\n    const highlights = {\n        'Vienna': [\n            { icon: '🎼', title: 'Cultural Heritage', description: 'UNESCO World Heritage historic center' },\n            { icon: '☕', title: 'Coffee Culture', description: 'Traditional Viennese coffee houses' },\n            { icon: '🏛️', title: 'Imperial Architecture', description: 'Stunning palaces and museums' },\n            { icon: '🎭', title: 'Arts Scene', description: 'World-class opera and theaters' }\n        ],\n        'Paris': [\n            { icon: '🗼', title: 'Iconic Landmarks', description: 'Eiffel Tower and Notre-Dame' },\n            { icon: '🍷', title: 'Culinary Excellence', description: 'World\'s finest restaurants' },\n            { icon: '👗', title: 'Fashion Capital', description: 'Global fashion and luxury hub' },\n            { icon: '🎨', title: 'Art & Culture', description: 'Louvre and countless galleries' }\n        ],\n        'Berlin': [\n            { icon: '🚀', title: 'Startup Hub', description: 'Europe\'s leading tech ecosystem' },\n            { icon: '🧱', title: 'Historical Significance', description: 'Rich 20th century history' },\n            { icon: '🎵', title: 'Music Scene', description: 'Vibrant nightlife and clubs' },\n            { icon: '🌍', title: 'International City', description: 'Diverse and cosmopolitan' }\n        ],\n        'Rome': [\n            { icon: '🏛️', title: 'Ancient History', description: 'Colosseum and Roman Forum' },\n            { icon: '🍝', title: 'Authentic Cuisine', description: 'Traditional Italian flavors' },\n            { icon: '⛪', title: 'Vatican City', description: 'St. Peter\\'s and Sistine Chapel' },\n            { icon: '🎬', title: 'Cinema History', description: 'Cinecittà film studios' }\n        ],\n        'Madrid': [\n            { icon: '🏛️', title: 'Royal Heritage', description: 'Royal Palace and gardens' },\n            { icon: '🎨', title: 'Art Triangle', description: 'Prado, Reina Sofia, Thyssen' },\n            { icon: '🌅', title: 'Vibrant Lifestyle', description: 'Late-night dining culture' },\n            { icon: '⚽', title: 'Football Culture', description: 'Real Madrid and Atletico' }\n        ]\n    };\n    \n    const cityHighlights = highlights[cityName] || highlights['Vienna'];\n    const container = document.getElementById('highlights-container');\n    \n    container.innerHTML = cityHighlights.map(highlight => `\n        <div class=\"highlight-card\">\n            <span class=\"highlight-icon\">${highlight.icon}</span>\n            <h4 class=\"highlight-title\">${highlight.title}</h4>\n            <p class=\"highlight-description\">${highlight.description}</p>\n        </div>\n    `).join('');\n}\n\nfunction initializeCitySearch(countryCode, cityName) {\n    const searchInput = document.getElementById('local-search-input');\n    const searchBtn = document.getElementById('local-search-btn');\n    \n    const performSearch = () => {\n        const query = searchInput.value.trim();\n        const category = document.getElementById('category-filter').value;\n        const distance = document.getElementById('distance-filter').value;\n        \n        if (!query && !category) {\n            alert('Please enter a search term or select a category');\n            return;\n        }\n        \n        // Build search URL\n        const params = new URLSearchParams();\n        if (query) params.append('q', query);\n        if (category) params.append('category', category);\n        if (distance) params.append('distance', distance);\n        params.append('city', cityName);\n        params.append('country', countryCode);\n        \n        window.location.href = `search-results.html?${params.toString()}`;\n    };\n    \n    searchBtn.addEventListener('click', performSearch);\n    searchInput.addEventListener('keypress', (e) => {\n        if (e.key === 'Enter') performSearch();\n    });\n}\n\n// Utility Functions\nfunction showMap() {\n    alert('Interactive map integration coming soon!');\n}\n\nfunction scrollToSearch() {\n    document.querySelector('.search-section').scrollIntoView({ behavior: 'smooth' });\n}\n\nfunction filterByCategory(category) {\n    // Update active state\n    document.querySelectorAll('.category-chip').forEach(chip => {\n        chip.classList.remove('active');\n        if (chip.dataset.category === category) {\n            chip.classList.add('active');\n        }\n    });\n    \n    // Filter businesses (in a real app, this would filter the actual results)\n    console.log(`Filtering by category: ${category}`);\n}\n\nfunction searchNearbyCity(cityName) {\n    const [city, country] = cityName.split(', ');\n    const countryCode = getCountryCodeByName(country);\n    \n    if (countryCode) {\n        window.location.href = `city.html?country=${countryCode}&city=${encodeURIComponent(city)}`;\n    }\n}\n\nfunction getCountryName(code) {\n    const countryNames = {\n        'at': 'Austria', 'be': 'Belgium', 'bg': 'Bulgaria', 'hr': 'Croatia',\n        'cy': 'Cyprus', 'cz': 'Czechia', 'dk': 'Denmark', 'ee': 'Estonia',\n        'fi': 'Finland', 'fr': 'France', 'de': 'Germany', 'gr': 'Greece',\n        'hu': 'Hungary', 'ie': 'Ireland', 'it': 'Italy', 'lv': 'Latvia',\n        'lt': 'Lithuania', 'lu': 'Luxembourg', 'mt': 'Malta', 'nl': 'Netherlands',\n        'pl': 'Poland', 'pt': 'Portugal', 'ro': 'Romania', 'sk': 'Slovakia',\n        'si': 'Slovenia', 'es': 'Spain', 'se': 'Sweden'\n    };\n    return countryNames[code] || 'Austria';\n}\n\nfunction getCountryCodeByName(countryName) {\n    const countryCodes = {\n        'Austria': 'at', 'Belgium': 'be', 'Bulgaria': 'bg', 'Croatia': 'hr',\n        'Cyprus': 'cy', 'Czechia': 'cz', 'Denmark': 'dk', 'Estonia': 'ee',\n        'Finland': 'fi', 'France': 'fr', 'Germany': 'de', 'Greece': 'gr',\n        'Hungary': 'hu', 'Ireland': 'ie', 'Italy': 'it', 'Latvia': 'lv',\n        'Lithuania': 'lt', 'Luxembourg': 'lu', 'Malta': 'mt', 'Netherlands': 'nl',\n        'Poland': 'pl', 'Portugal': 'pt', 'Romania': 'ro', 'Slovakia': 'sk',\n        'Slovenia': 'si', 'Spain': 'es', 'Sweden': 'se', 'UK': 'gb'\n    };\n    return countryCodes[countryName];\n}