// Search Results Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Parse URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const searchQuery = urlParams.get('q') || '';
    const country = urlParams.get('country') || '';
    const city = urlParams.get('city') || '';
    const category = urlParams.get('category') || '';
    
    // Initialize page
    initializeSearchResults(searchQuery, { country, city, category });
    
    // Setup filters
    setupFilters();
    
    // Setup view switching
    setupViewSwitching();
    
    // Setup sorting
    setupSorting();
});

function initializeSearchResults(query, filters) {
    // Update search header
    updateSearchHeader(query, filters);
    
    // Show current search tags
    displayCurrentSearch(query, filters);
    
    // Load and display results
    loadSearchResults(query, filters);
    
    // Load related suggestions
    loadSearchSuggestions(query);
    
    // Populate filter options
    populateFilters();
}

function updateSearchHeader(query, filters) {
    let title = 'Search Results';
    let description = '';
    
    if (query) {
        title = `Results for "${query}"`;
        description = `Search results for ${query}`;
    }
    
    if (filters.city && filters.country) {
        const countryName = getCountryName(filters.country);
        description += ` in ${filters.city}, ${countryName}`;
    } else if (filters.country) {
        const countryName = getCountryName(filters.country);
        description += ` in ${countryName}`;
    }
    
    if (filters.category) {
        description += ` - ${filters.category} category`;
    }
    
    document.getElementById('search-title').textContent = title;
    document.title = `${title} | ListAcross EU`;
    
    if (description) {
        const metaDesc = document.querySelector('meta[name="description"]');
        if (metaDesc) {
            metaDesc.setAttribute('content', description);
        }
    }
}

function displayCurrentSearch(query, filters) {
    const container = document.getElementById('search-tags');
    const tags = [];
    
    if (query) {
        tags.push({
            type: 'query',
            label: `"${query}"`,
            value: query
        });
    }
    
    if (filters.country) {
        const countryName = getCountryName(filters.country);
        tags.push({
            type: 'country',
            label: countryName,
            value: filters.country
        });
    }
    
    if (filters.city) {
        tags.push({
            type: 'city',
            label: filters.city,
            value: filters.city
        });
    }
    
    if (filters.category) {
        tags.push({
            type: 'category',
            label: filters.category,
            value: filters.category
        });
    }
    
    container.innerHTML = tags.map(tag => `
        <span class="search-tag">
            ${tag.label}
            <span class="remove" onclick="removeSearchTag('${tag.type}')">×</span>
        </span>
    `).join('');
}

function loadSearchResults(query, filters) {
    // Demo search results
    const allResults = [
        {
            id: 1,
            name: 'Café Central Vienna',
            category: 'Restaurant',
            location: 'Vienna, Austria',
            address: 'Herrengasse 14, 1010 Vienna',
            rating: 4.5,
            reviewCount: 1247,
            description: 'Historic Viennese coffeehouse serving traditional Austrian cuisine and world-famous coffee since 1876.',
            phone: '+43 1 533 3763',
            website: 'www.cafecentral.wien',
            country: 'at',
            city: 'Vienna'
        },
        {
            id: 2,
            name: 'La Brasserie du Marché',
            category: 'Restaurant',
            location: 'Paris, France',
            address: '15 Rue des Martyrs, 75009 Paris',
            rating: 4.7,
            reviewCount: 892,
            description: 'Authentic French brasserie in the heart of Montmartre, serving traditional French cuisine.',
            phone: '+33 1 48 78 62 73',
            website: 'www.brasseriedumarche.fr',
            country: 'fr',
            city: 'Paris'
        },
        {
            id: 3,
            name: 'Berlin Tech Solutions GmbH',
            category: 'Technology',
            location: 'Berlin, Germany',
            address: 'Alexanderplatz 1, 10178 Berlin',
            rating: 4.3,
            reviewCount: 156,
            description: 'Leading IT consulting and software development company specializing in fintech solutions.',
            phone: '+49 30 12345678',
            website: 'www.berlintech-solutions.de',
            country: 'de',
            city: 'Berlin'
        },
        {
            id: 4,
            name: 'Trattoria Bella Napoli',
            category: 'Restaurant',
            location: 'Rome, Italy',
            address: 'Via Roma 23, 00187 Rome',
            rating: 4.8,
            reviewCount: 2341,
            description: 'Authentic Neapolitan cuisine in the heart of Rome. Fresh pasta made daily, wood-fired pizza.',
            phone: '+39 06 1234567',
            website: 'www.trattoriabellanapoli.it',
            country: 'it',
            city: 'Rome'
        },
        {
            id: 5,
            name: 'Amsterdam Bike Rental',
            category: 'Tourism',
            location: 'Amsterdam, Netherlands',
            address: 'Damrak 62, 1012 LM Amsterdam',
            rating: 4.6,
            reviewCount: 743,
            description: 'Premium bike rental service in Amsterdam city center. Electric bikes and guided tours available.',
            phone: '+31 20 1234567',
            website: 'www.amsterdambike-rental.nl',
            country: 'nl',
            city: 'Amsterdam'
        }
    ];
    
    // Filter results based on search criteria
    let filteredResults = allResults.filter(result => {
        let matches = true;
        
        if (query) {
            const searchTerms = query.toLowerCase();
            matches = matches && (
                result.name.toLowerCase().includes(searchTerms) ||
                result.category.toLowerCase().includes(searchTerms) ||
                result.description.toLowerCase().includes(searchTerms) ||
                result.location.toLowerCase().includes(searchTerms)
            );
        }
        
        if (filters.country) {
            matches = matches && result.country === filters.country;
        }
        
        if (filters.city) {
            matches = matches && result.city.toLowerCase().includes(filters.city.toLowerCase());
        }
        
        if (filters.category) {
            matches = matches && result.category.toLowerCase().includes(filters.category.toLowerCase());
        }
        
        return matches;
    });
    
    // Update results count
    document.getElementById('results-count').textContent = `${filteredResults.length} results found`;
    
    // Display results or no results message
    if (filteredResults.length === 0) {
        showNoResults();
    } else {
        displayResults(filteredResults);
    }
}

function displayResults(results) {
    const container = document.getElementById('results-container');
    document.getElementById('no-results').style.display = 'none';
    
    container.innerHTML = results.map(result => `
        <div class="result-item" onclick="window.location.href='business-listing.html?id=${result.id}'">
            <div class="result-header">
                <h3 class="result-title">${result.name}</h3>
                <span class="result-category">${result.category}</span>
            </div>
            <div class="result-location">📍 ${result.location}</div>
            <div class="result-rating">
                <span class="stars">${'★'.repeat(Math.floor(result.rating))}${'☆'.repeat(5-Math.floor(result.rating))}</span>
                <span>${result.rating} (${result.reviewCount} reviews)</span>
            </div>
            <p class="result-description">${result.description}</p>
            <div class="result-meta">
                <span>📞 ${result.phone}</span>
                <span>🌐 ${result.website}</span>
            </div>
        </div>
    `).join('');
    
    // Show pagination if needed
    if (results.length > 10) {
        showPagination(results.length);
    }
}

function showNoResults() {
    document.getElementById('results-container').innerHTML = '';
    document.getElementById('no-results').style.display = 'block';
}

function showPagination(totalResults) {
    const container = document.getElementById('pagination');
    const totalPages = Math.ceil(totalResults / 10);
    const currentPage = 1;
    
    if (totalPages <= 1) return;
    
    let paginationHTML = '';
    
    // Previous button
    if (currentPage > 1) {
        paginationHTML += '<a href="#" class="page-btn">← Previous</a>';
    }
    
    // Page numbers
    for (let i = 1; i <= Math.min(totalPages, 10); i++) {
        const activeClass = i === currentPage ? ' active' : '';
        paginationHTML += `<a href="#" class="page-btn${activeClass}">${i}</a>`;
    }
    
    // Next button
    if (currentPage < totalPages) {
        paginationHTML += '<a href="#" class="page-btn">Next →</a>';
    }
    
    container.innerHTML = paginationHTML;
}

function loadSearchSuggestions(query) {
    const suggestions = [
        'restaurants in Vienna',
        'tech companies Berlin',
        'hotels Amsterdam',
        'cafes Paris',
        'IT services',
        'tourism Rome',
        'bike rental',
        'French cuisine'
    ];
    
    const container = document.getElementById('suggestions-list');
    
    container.innerHTML = suggestions.map(suggestion => `
        <span class="suggestion-tag" onclick="searchSuggestion('${suggestion}')">
            ${suggestion}
        </span>
    `).join('');
}

function populateFilters() {
    // Populate country filter
    const countries = [
        { code: 'at', name: 'Austria' },
        { code: 'fr', name: 'France' },
        { code: 'de', name: 'Germany' },
        { code: 'it', name: 'Italy' },
        { code: 'es', name: 'Spain' },
        { code: 'nl', name: 'Netherlands' }
    ];
    
    const countryFilter = document.getElementById('country-filter');
    countryFilter.innerHTML = '<option value="">Any Country</option>' + 
        countries.map(country => `<option value="${country.code}">${country.name}</option>`).join('');
    
    // Populate category checkboxes
    const categories = [
        'Restaurant', 'Technology', 'Tourism', 'Retail', 'Healthcare', 'Services'
    ];
    
    const categoryContainer = document.getElementById('category-checkboxes');
    categoryContainer.innerHTML = categories.map(category => `
        <label>
            <input type="checkbox" value="${category.toLowerCase()}"> ${category}
        </label>
    `).join('');
}

function setupFilters() {
    // Apply filters button
    window.applyFilters = function() {
        const params = new URLSearchParams(window.location.search);
        
        // Get filter values
        const country = document.getElementById('country-filter').value;
        const city = document.getElementById('city-filter').value;
        const rating = document.querySelector('input[name="rating"]:checked')?.value;
        const distance = document.getElementById('distance-filter').value;
        
        // Get selected categories
        const selectedCategories = Array.from(document.querySelectorAll('#category-checkboxes input:checked'))
            .map(cb => cb.value);
        
        // Update URL parameters
        if (country) params.set('country', country);
        else params.delete('country');
        
        if (city) params.set('city', city);
        else params.delete('city');
        
        if (selectedCategories.length > 0) {
            params.set('category', selectedCategories.join(','));
        } else {
            params.delete('category');
        }
        
        if (rating) params.set('rating', rating);
        else params.delete('rating');
        
        if (distance) params.set('distance', distance);
        else params.delete('distance');
        
        // Reload page with new filters
        window.location.search = params.toString();
    };
    
    // Clear filters button
    window.clearFilters = function() {
        const params = new URLSearchParams(window.location.search);
        
        // Keep only the search query
        const query = params.get('q');
        const newParams = new URLSearchParams();
        if (query) newParams.set('q', query);
        
        window.location.search = newParams.toString();
    };
    
    // Show/hide filters on mobile
    window.showFilters = function() {
        const filters = document.getElementById('search-filters');
        filters.style.display = filters.style.display === 'none' ? 'block' : 'none';
    };
}

function setupViewSwitching() {
    const viewBtns = document.querySelectorAll('.view-btn');
    const container = document.getElementById('results-container');
    
    viewBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active button
            viewBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Update container class
            const view = btn.dataset.view;
            container.className = 'results-container';
            
            if (view === 'grid') {
                container.classList.add('grid-view');
            } else if (view === 'map') {
                container.classList.add('map-view');
                showMapView();
            }
        });
    });
}

function showMapView() {
    const container = document.getElementById('results-container');
    container.innerHTML = `
        <div class="map-container">
            <div style="text-align: center; color: var(--muted);">
                🗺️ Interactive Map View<br>
                <small>Business locations will be displayed here</small>
            </div>
        </div>
        <div class="map-results">
            <div style="padding: 20px; text-align: center; color: var(--muted);">
                <h4>Results List</h4>
                <p>Click on map markers to see business details</p>
            </div>
        </div>
    `;
}

function setupSorting() {
    const sortSelect = document.getElementById('results-sort');
    
    sortSelect.addEventListener('change', (e) => {
        const sortBy = e.target.value;
        console.log(`Sorting by: ${sortBy}`);
        // In a real app, this would re-sort and re-display results
    });
}

// Utility Functions
function removeSearchTag(type) {
    const params = new URLSearchParams(window.location.search);
    
    switch (type) {
        case 'query':
            params.delete('q');
            break;
        case 'country':
            params.delete('country');
            break;
        case 'city':
            params.delete('city');
            break;
        case 'category':
            params.delete('category');
            break;
    }
    
    window.location.search = params.toString();
}

function searchSuggestion(suggestion) {
    const params = new URLSearchParams();
    params.set('q', suggestion);
    window.location.search = params.toString();
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
    return countryNames[code] || code.toUpperCase();
}