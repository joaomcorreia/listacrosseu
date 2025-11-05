// Country Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Get country from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const countryCode = urlParams.get('code') || 'at';
    const countryName = urlParams.get('name') || getCountryName(countryCode);
    
    // Load country data
    loadCountryData(countryCode, countryName);
    
    // Initialize search functionality
    initializeCountrySearch(countryCode);
    
    // Load cities
    loadCities(countryCode);
    
    // Load categories
    loadCategories(countryCode);
    
    // Load recent businesses
    loadRecentBusinesses(countryCode);
});

function loadCountryData(countryCode, countryName) {
    // Demo data for different countries
    const countryData = {
        'at': {
            name: 'Austria',
            description: 'Discover Austrian businesses from historic Vienna cafés to Alpine tourism services. Austria offers a rich business landscape combining traditional craftsmanship with modern innovation.',
            totalCities: 15,
            totalBusinesses: 12847,
            euJoinYear: 1995,
            restaurantCount: 2341,
            retailCount: 3892,
            servicesCount: 4521,
            tourismCount: 2093
        },
        'fr': {
            name: 'France',
            description: 'Explore French businesses from Parisian boutiques to Provence wineries. France leads Europe in luxury goods, gastronomy, and cultural tourism.',
            totalCities: 45,
            totalBusinesses: 89234,
            euJoinYear: 1957,
            restaurantCount: 15672,
            retailCount: 23891,
            servicesCount: 31245,
            tourismCount: 18426
        },
        'de': {
            name: 'Germany',
            description: 'Discover German businesses from Berlin startups to Bavarian manufacturers. Germany is Europe\'s economic powerhouse with excellence in engineering and technology.',
            totalCities: 52,
            totalBusinesses: 134567,
            euJoinYear: 1957,
            restaurantCount: 18934,
            retailCount: 34521,
            servicesCount: 52341,
            tourismCount: 28771
        },
        'it': {
            name: 'Italy',
            description: 'Explore Italian businesses from Roman trattorias to Milanese fashion houses. Italy combines centuries-old traditions with contemporary design and innovation.',
            totalCities: 38,
            totalBusinesses: 76543,
            euJoinYear: 1957,
            restaurantCount: 21456,
            retailCount: 19876,
            servicesCount: 23891,
            tourismCount: 11320
        },
        'es': {
            name: 'Spain',
            description: 'Discover Spanish businesses from Barcelona tech companies to Andalusian olive farms. Spain offers diverse opportunities across tourism, agriculture, and innovation.',
            totalCities: 42,
            totalBusinesses: 67891,
            euJoinYear: 1986,
            restaurantCount: 18765,
            retailCount: 17234,
            servicesCount: 21092,
            tourismCount: 10800
        }
    };
    
    const data = countryData[countryCode] || countryData['at'];
    
    // Update page content
    updateCountryContent(data, countryCode);
}

function updateCountryContent(data, countryCode) {
    // Update title and meta
    document.title = `${data.name} Business Directory | ListAcross EU`;
    
    // Update country header
    document.querySelector('.country-details h1').textContent = `Business Directory - ${data.name}`;
    document.querySelector('.country-description').textContent = data.description;
    document.querySelector('.country-flag img').src = `assets/flags/${countryCode}.png`;
    document.querySelector('.country-flag img').alt = `${data.name} flag`;
    
    // Update stats
    const stats = document.querySelectorAll('.country-meta .stat');
    if (stats.length >= 3) {
        stats[0].textContent = `📍 ${data.totalCities} Cities`;
        stats[1].textContent = `🏢 ${data.totalBusinesses.toLocaleString()} Businesses`;
        stats[2].textContent = `🌍 EU Member Since ${data.euJoinYear}`;
    }
    
    // Update search section
    document.querySelector('.search-section h2').textContent = `Find Businesses in ${data.name}`;
    
    // Update section titles
    document.querySelector('.cities-section h2').textContent = `Major Cities in ${data.name}`;
    document.querySelector('.country-stats h2').textContent = `${data.name} Business Statistics`;
    
    // Update statistics
    document.getElementById('total-restaurants').textContent = data.restaurantCount.toLocaleString();
    document.getElementById('total-retail').textContent = data.retailCount.toLocaleString();
    document.getElementById('total-services').textContent = data.servicesCount.toLocaleString();
    document.getElementById('total-tourism').textContent = data.tourismCount.toLocaleString();
    
    // Update upgrade section
    document.querySelector('.upgrade-banner h3').textContent = `Business Owner in ${data.name}?`;
    document.querySelector('.upgrade-banner .plan-card:nth-child(2) p').textContent = `Visibility across all of ${data.name}`;
    
    // Update breadcrumb
    document.querySelector('.breadcrumb span').textContent = data.name;
}

function loadCities(countryCode) {
    const citiesData = {
        'at': [
            { name: 'Vienna', businesses: 4521, description: 'Austria\'s capital and cultural center' },
            { name: 'Salzburg', businesses: 1892, description: 'Mozart\'s birthplace and UNESCO heritage city' },
            { name: 'Innsbruck', businesses: 1456, description: 'Alpine city and winter sports destination' },
            { name: 'Graz', businesses: 1234, description: 'University town and architectural gem' },
            { name: 'Linz', businesses: 987, description: 'Industrial hub on the Danube River' }
        ],
        'fr': [
            { name: 'Paris', businesses: 25431, description: 'Capital of fashion, cuisine, and culture' },
            { name: 'Marseille', businesses: 8765, description: 'Mediterranean port and multicultural hub' },
            { name: 'Lyon', businesses: 6543, description: 'Gastronomic capital and silk city' },
            { name: 'Toulouse', businesses: 4321, description: 'Aerospace industry center' },
            { name: 'Nice', businesses: 3876, description: 'French Riviera resort destination' }
        ],
        'de': [
            { name: 'Berlin', businesses: 18765, description: 'Capital city and startup hub' },
            { name: 'Hamburg', businesses: 12343, description: 'Port city and media center' },
            { name: 'Munich', businesses: 14567, description: 'Bavarian capital and tech center' },
            { name: 'Cologne', businesses: 9876, description: 'Cultural metropolis on the Rhine' },
            { name: 'Frankfurt', businesses: 11234, description: 'Financial capital of Europe' }
        ],
        'it': [
            { name: 'Rome', businesses: 15432, description: 'Eternal city and government center' },
            { name: 'Milan', businesses: 18765, description: 'Fashion and business capital' },
            { name: 'Naples', businesses: 8901, description: 'Southern cultural powerhouse' },
            { name: 'Turin', businesses: 6543, description: 'Industrial and automotive hub' },
            { name: 'Florence', businesses: 4321, description: 'Renaissance art and culture center' }
        ],
        'es': [
            { name: 'Madrid', businesses: 16789, description: 'Capital and business center' },
            { name: 'Barcelona', businesses: 14567, description: 'Mediterranean cultural capital' },
            { name: 'Valencia', businesses: 7890, description: 'Third largest city and port' },
            { name: 'Seville', businesses: 5432, description: 'Andalusian cultural heart' },
            { name: 'Bilbao', businesses: 4321, description: 'Basque industrial and cultural center' }
        ]
    };
    
    const cities = citiesData[countryCode] || citiesData['at'];
    const container = document.getElementById('cities-container');
    
    container.innerHTML = cities.map(city => `
        <div class="city-card" onclick="window.location.href='city.html?country=${countryCode}&city=${encodeURIComponent(city.name)}'">
            <div class="city-card-image">🏙️</div>
            <div class="city-card-content">
                <h3 class="city-name">${city.name}</h3>
                <div class="city-stats">
                    <span>${city.businesses.toLocaleString()} businesses</span>
                    <span>View all →</span>
                </div>
                <p class="city-description">${city.description}</p>
            </div>
        </div>
    `).join('');
    
    // Populate city filter
    const cityFilter = document.getElementById('city-filter');
    cityFilter.innerHTML = '<option value="">All Cities</option>' + 
        cities.map(city => `<option value="${city.name}">${city.name}</option>`).join('');
}

function loadCategories(countryCode) {
    const categories = [
        { name: 'Restaurants & Cafés', icon: '🍽️', count: 2341, description: 'Dining and hospitality' },
        { name: 'Retail & Shopping', icon: '🛍️', count: 3892, description: 'Stores and boutiques' },
        { name: 'Professional Services', icon: '💼', count: 4521, description: 'Business and consulting' },
        { name: 'Tourism & Hotels', icon: '🏨', count: 2093, description: 'Hospitality and travel' },
        { name: 'Healthcare', icon: '🏥', count: 1876, description: 'Medical and wellness' },
        { name: 'Technology', icon: '💻', count: 1567, description: 'IT and digital services' },
        { name: 'Automotive', icon: '🚗', count: 987, description: 'Car services and dealers' },
        { name: 'Real Estate', icon: '🏠', count: 1234, description: 'Property and rentals' }
    ];
    
    const container = document.getElementById('categories-container');
    
    container.innerHTML = categories.map(category => `
        <div class="category-card" onclick="searchByCategory('${category.name.toLowerCase()}')">
            <span class="category-icon">${category.icon}</span>
            <h3 class="category-name">${category.name}</h3>
            <p class="category-count">${category.count.toLocaleString()} businesses</p>
        </div>
    `).join('');
}

function loadRecentBusinesses(countryCode) {
    const businesses = [
        { name: 'Alpine Wellness Spa', category: 'Healthcare', city: 'Innsbruck', rating: 4.8 },
        { name: 'TechStart Vienna', category: 'Technology', city: 'Vienna', rating: 4.6 },
        { name: 'Café Mozart', category: 'Restaurant', city: 'Salzburg', rating: 4.7 },
        { name: 'Fashion Boutique Graz', category: 'Retail', city: 'Graz', rating: 4.5 },
        { name: 'Danube Tours', category: 'Tourism', city: 'Linz', rating: 4.9 },
        { name: 'Business Consulting Pro', category: 'Services', city: 'Vienna', rating: 4.4 }
    ];
    
    const container = document.getElementById('recent-businesses');
    
    container.innerHTML = businesses.map((business, index) => `
        <div class="business-preview" onclick="window.location.href='business-listing.html?id=${index + 2}'">
            <div class="business-preview-header">
                <h3 class="business-preview-name">${business.name}</h3>
                <span class="business-preview-category">${business.category}</span>
            </div>
            <div class="business-preview-location">📍 ${business.city}</div>
            <div class="business-preview-rating">${'★'.repeat(Math.floor(business.rating))}☆ ${business.rating}</div>
        </div>
    `).join('');
}

function initializeCountrySearch(countryCode) {
    const searchInput = document.getElementById('country-search-input');
    const searchBtn = document.getElementById('search-btn');
    const cityFilter = document.getElementById('city-filter');
    const categoryFilter = document.getElementById('category-filter');
    
    const performSearch = () => {
        const query = searchInput.value.trim();
        const city = cityFilter.value;
        const category = categoryFilter.value;
        
        if (!query && !city && !category) {
            alert('Please enter a search term or select filters');
            return;
        }
        
        // Build search URL
        const params = new URLSearchParams();
        if (query) params.append('q', query);
        if (city) params.append('city', city);
        if (category) params.append('category', category);
        params.append('country', countryCode);
        
        window.location.href = `search-results.html?${params.toString()}`;
    };
    
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performSearch();
    });
}

function searchByCategory(category) {
    const urlParams = new URLSearchParams(window.location.search);
    const countryCode = urlParams.get('code') || 'at';
    
    window.location.href = `search-results.html?category=${encodeURIComponent(category)}&country=${countryCode}`;
}

function getCountryName(code) {
    const countryNames = {
        'at': 'Austria',
        'be': 'Belgium',
        'bg': 'Bulgaria',
        'hr': 'Croatia',
        'cy': 'Cyprus',
        'cz': 'Czechia',
        'dk': 'Denmark',
        'ee': 'Estonia',
        'fi': 'Finland',
        'fr': 'France',
        'de': 'Germany',
        'gr': 'Greece',
        'hu': 'Hungary',
        'ie': 'Ireland',
        'it': 'Italy',
        'lv': 'Latvia',
        'lt': 'Lithuania',
        'lu': 'Luxembourg',
        'mt': 'Malta',
        'nl': 'Netherlands',
        'pl': 'Poland',
        'pt': 'Portugal',
        'ro': 'Romania',
        'sk': 'Slovakia',
        'si': 'Slovenia',
        'es': 'Spain',
        'se': 'Sweden'
    };
    
    return countryNames[code] || 'Austria';
}