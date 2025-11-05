/* Enhanced map functionality for ListAcrossEU */

// Map configuration and dynamic loading
class MapManager {
  constructor() {
    this.currentMap = null;
    this.mapContainer = null;
    this.searchInput = null;
    this.init();
  }

  init() {
    this.mapContainer = document.querySelector('.map-embed');
    this.searchInput = document.querySelector('#map-search');

    if (this.mapContainer) {
      this.setupMapInteraction();
    }

    if (this.searchInput) {
      this.setupSearch();
    }
  }

  setupMapInteraction() {
    // Add map interaction hints
    const mapWrap = document.querySelector('.map-wrap');
    if (mapWrap) {
      mapWrap.addEventListener('mouseenter', () => {
        mapWrap.style.cursor = 'pointer';
      });
    }
  }

  setupSearch() {
    let searchTimeout;

    this.searchInput.addEventListener('input', (e) => {
      clearTimeout(searchTimeout);
      const query = e.target.value.trim();

      if (query.length >= 2) {
        searchTimeout = setTimeout(() => {
          this.performSearch(query);
        }, 300);
      }
    });
  }

  async performSearch(query) {
    try {
      // This would connect to your Django backend
      const response = await fetch(`/api/search/?q=${encodeURIComponent(query)}`);
      const results = await response.json();

      this.displaySearchResults(results);
    } catch (error) {
      console.log('Search not available yet:', error);
    }
  }

  displaySearchResults(results) {
    // Create or update search results dropdown
    let dropdown = document.querySelector('.search-dropdown');

    if (!dropdown) {
      dropdown = document.createElement('div');
      dropdown.className = 'search-dropdown';
      this.searchInput.parentNode.appendChild(dropdown);
    }

    dropdown.innerHTML = '';

    if (results.length === 0) {
      dropdown.innerHTML = '<div class="no-results">No results found</div>';
      return;
    }

    results.forEach(result => {
      const item = document.createElement('div');
      item.className = 'search-result-item';
      item.innerHTML = `
        <strong>${result.name}</strong>
        <span>${result.location}</span>
      `;
      item.addEventListener('click', () => {
        window.location.href = result.url;
      });
      dropdown.appendChild(item);
    });
  }

  // Update map for different locations
  updateMap(locationType, locationCode) {
    if (!this.mapContainer) return;

    const coordinates = this.getCoordinates(locationType, locationCode);
    const newMapUrl = this.generateMapUrl(coordinates);

    // Smooth transition between maps
    this.mapContainer.style.opacity = '0.7';

    setTimeout(() => {
      this.mapContainer.src = newMapUrl;
      this.mapContainer.onload = () => {
        this.mapContainer.style.opacity = '1';
      };
    }, 200);
  }

  getCoordinates(locationType, locationCode) {
    // Use the coordinates from the template or defaults
    if (window.mapConfig && window.mapConfig.coordinates) {
      return window.mapConfig.coordinates;
    }

    // Fallback coordinates
    const defaultCoords = {
      europe: { lat: 54.5260, lng: 15.2551, zoom: 4 },
      countries: {
        'AT': { lat: 47.5162, lng: 14.5501, zoom: 7 },
        'PT': { lat: 39.3999, lng: -8.2245, zoom: 7 },
        // Add more as needed
      },
      cities: {
        'porto': { lat: 41.1579, lng: -8.6291, zoom: 12 },
        'lisbon': { lat: 38.7223, lng: -9.1393, zoom: 12 },
        // Add more as needed
      }
    };

    if (locationType === 'country') {
      return defaultCoords.countries[locationCode.toUpperCase()] || defaultCoords.europe;
    } else if (locationType === 'city') {
      return defaultCoords.cities[locationCode.toLowerCase()] || defaultCoords.europe;
    }

    return defaultCoords.europe;
  }

  generateMapUrl(coordinates) {
    const { lat, lng, zoom } = coordinates;
    const params = `!1m14!1m12!1m3!1d44136871.028996035!2d${lng}!3d${lat}!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1sen!2s!4v0000000000000`;
    return `https://www.google.com/maps/embed?pb=${params}`;
  }
}

// Global search function for search button
function performMapSearch() {
  const searchInput = document.querySelector('#map-search');
  const locationFilter = document.querySelector('#location-filter');
  const categoryFilter = document.querySelector('#category-filter');

  const query = searchInput?.value?.trim() || '';
  const location = locationFilter?.value || 'europe';
  const category = categoryFilter?.value || '';

  // Build search URL
  let searchUrl = '/businesses/?';
  const params = new URLSearchParams();

  if (query) params.append('q', query);
  if (location !== 'europe') params.append('location', location);
  if (category) params.append('category', category);

  searchUrl += params.toString();

  // Navigate to search results
  window.location.href = searchUrl;
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
  window.mapManager = new MapManager();

  // Setup enter key for search
  const searchInput = document.querySelector('#map-search');
  if (searchInput) {
    searchInput.addEventListener('keypress', function (e) {
      if (e.key === 'Enter') {
        performMapSearch();
      }
    });
  }
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { MapManager, performMapSearch };
}