// City Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const countryCode = urlParams.get('country') || 'at';
    const cityName = urlParams.get('city') || 'Vienna';
    
    loadCityData(countryCode, cityName);
    initializeCitySearch(countryCode, cityName);
    loadQuickCategories();
    loadCityBusinesses(countryCode, cityName);
    loadNearbyCities(countryCode, cityName);
    loadCityHighlights(cityName);
});

function loadCityData(countryCode, cityName) {
    const cityData = {
        'Vienna': {
            population: '1.9M',
            totalBusinesses: 4521,
            avgRating: 4.6,
            description: 'Austria elegant capital combining imperial grandeur with modern innovation.'
        },
        'Paris': {
            population: '2.2M',
            totalBusinesses: 25431,
            avgRating: 4.4,
            description: 'The City of Light offers unparalleled business opportunities in fashion and cuisine.'
        }
    };
    
    const data = cityData[cityName] || cityData['Vienna'];
    const countryName = getCountryName(countryCode);
    updateCityContent(data, cityName, countryName, countryCode);
}

function updateCityContent(data, cityName, countryName, countryCode) {
    document.title = cityName + ', ' + countryName + ' - Business Directory | ListAcross EU';
    
    document.getElementById('city-title').textContent = 'Businesses in ' + cityName + ', ' + countryName;
    document.getElementById('total-businesses').textContent = data.totalBusinesses.toLocaleString();
    document.getElementById('avg-rating').textContent = data.avgRating;
    document.getElementById('city-population').textContent = data.population;
    document.getElementById('city-description').textContent = data.description;
    
    document.getElementById('country-link').textContent = countryName;
    document.getElementById('country-link').href = 'country.html?code=' + countryCode + '&name=' + encodeURIComponent(countryName);
    document.getElementById('city-name').textContent = cityName;
    
    document.getElementById('city-name-categories').textContent = cityName;
    document.getElementById('map-city-name').textContent = cityName;
    document.getElementById('city-name-highlights').textContent = cityName;
    document.getElementById('upgrade-city-name').textContent = cityName;
    document.getElementById('benefit-city-name').textContent = cityName;
}

function loadQuickCategories() {
    const categories = [
        { name: 'Restaurants', icon: '🍽️' },
        { name: 'Shopping', icon: '🛍️' },
        { name: 'Services', icon: '💼' },
        { name: 'Healthcare', icon: '🏥' },
        { name: 'Tourism', icon: '🏨' },
        { name: 'Technology', icon: '💻' }
    ];
    
    const container = document.getElementById('categories-container');
    container.innerHTML = categories.map(category => 
        '<div class="category-chip" onclick="filterByCategory(\'' + category.name.toLowerCase() + '\')" data-category="' + category.name.toLowerCase() + '">' +
        category.icon + ' ' + category.name + '</div>'
    ).join('');
}

function loadCityBusinesses(countryCode, cityName) {
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
            description: 'Historic Viennese coffeehouse serving traditional Austrian cuisine.'
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
            description: 'Leading IT consulting firm specializing in digital transformation.'
        }
    ];
    
    const container = document.getElementById('businesses-list');
    container.innerHTML = businesses.map(business => 
        '<div class="business-item" onclick="window.location.href=\'business-listing.html?id=' + business.id + '\'">' +
        '<div class="business-header">' +
        '<h3 class="business-name">' + business.name + '</h3>' +
        '<span class="business-category">' + business.category + '</span>' +
        '</div>' +
        '<div class="business-details">' +
        '<div class="business-location">📍 ' + business.address + '</div>' +
        '<div class="business-phone">📞 ' + business.phone + '</div>' +
        '<div class="business-hours">🕐 ' + business.hours + '</div>' +
        '</div>' +
        '<div class="business-rating">' +
        '<span class="stars">' + '★'.repeat(Math.floor(business.rating)) + '☆'.repeat(5-Math.floor(business.rating)) + '</span>' +
        '<span>' + business.rating + ' (' + business.reviewCount + ' reviews)</span>' +
        '</div>' +
        '<p class="business-description">' + business.description + '</p>' +
        '</div>'
    ).join('');
}

function loadNearbyCities(countryCode, cityName) {
    const nearbyCities = {
        'Vienna': ['Bratislava, Slovakia', 'Brno, Czechia', 'Graz, Austria'],
        'Paris': ['Brussels, Belgium', 'London, UK', 'Lyon, France']
    };
    
    const cities = nearbyCities[cityName] || nearbyCities['Vienna'];
    const container = document.getElementById('nearby-cities-list');
    
    container.innerHTML = cities.map(city => 
        '<div class="nearby-city" onclick="searchNearbyCity(\'' + city + '\')">' + city + '</div>'
    ).join('');
}

function loadCityHighlights(cityName) {
    const highlights = {
        'Vienna': [
            { icon: '🎼', title: 'Cultural Heritage', description: 'UNESCO World Heritage historic center' },
            { icon: '☕', title: 'Coffee Culture', description: 'Traditional Viennese coffee houses' }
        ],
        'Paris': [
            { icon: '🗼', title: 'Iconic Landmarks', description: 'Eiffel Tower and Notre-Dame' },
            { icon: '🍷', title: 'Culinary Excellence', description: 'World finest restaurants' }
        ]
    };
    
    const cityHighlights = highlights[cityName] || highlights['Vienna'];
    const container = document.getElementById('highlights-container');
    
    container.innerHTML = cityHighlights.map(highlight => 
        '<div class="highlight-card">' +
        '<span class="highlight-icon">' + highlight.icon + '</span>' +
        '<h4 class="highlight-title">' + highlight.title + '</h4>' +
        '<p class="highlight-description">' + highlight.description + '</p>' +
        '</div>'
    ).join('');
}

function initializeCitySearch(countryCode, cityName) {
    const searchInput = document.getElementById('local-search-input');
    const searchBtn = document.getElementById('local-search-btn');
    
    searchBtn.addEventListener('click', function() {
        const query = searchInput.value.trim();
        if (query) {
            const params = new URLSearchParams();
            params.append('q', query);
            params.append('city', cityName);
            params.append('country', countryCode);
            window.location.href = 'search-results.html?' + params.toString();
        }
    });
}

function showMap() {
    alert('Interactive map integration coming soon!');
}

function scrollToSearch() {
    document.querySelector('.search-section').scrollIntoView({ behavior: 'smooth' });
}

function filterByCategory(category) {
    document.querySelectorAll('.category-chip').forEach(chip => {
        chip.classList.remove('active');
        if (chip.dataset.category === category) {
            chip.classList.add('active');
        }
    });
}

function searchNearbyCity(cityName) {
    const parts = cityName.split(', ');
    const city = parts[0];
    const country = parts[1];
    const countryCode = getCountryCodeByName(country);
    
    if (countryCode) {
        window.location.href = 'city.html?country=' + countryCode + '&city=' + encodeURIComponent(city);
    }
}

function getCountryName(code) {
    const countryNames = {
        'at': 'Austria', 'fr': 'France', 'de': 'Germany', 
        'it': 'Italy', 'es': 'Spain', 'nl': 'Netherlands'
    };
    return countryNames[code] || 'Austria';
}

function getCountryCodeByName(countryName) {
    const countryCodes = {
        'Austria': 'at', 'France': 'fr', 'Germany': 'de',
        'Italy': 'it', 'Spain': 'es', 'Netherlands': 'nl',
        'Slovakia': 'sk', 'Czechia': 'cz', 'Belgium': 'be', 'UK': 'gb'
    };
    return countryCodes[countryName];
}