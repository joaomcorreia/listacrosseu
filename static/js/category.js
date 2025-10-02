// Category Page JavaScript
class CategoryPage {
  constructor() {
    this.currentCategory = this.getCategoryFromURL();
    this.businesses = [];
    this.subcategories = [];
    this.countries = [];
    this.cities = [];
    this.insights = [];
    
    this.init();
  }

  async init() {
    await this.loadCategoryData();
    this.setupEventListeners();
    this.populatePage();
  }

  getCategoryFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('category') || 'restaurants';
  }

  async loadCategoryData() {
    try {
      // In a real application, this would be API calls
      // For demo purposes, we'll use static data
      this.businesses = this.generateDemoBusinesses();
      this.subcategories = this.generateDemoSubcategories();
      this.countries = this.generateDemoCountries();
      this.cities = this.generateDemoCities();
      this.insights = this.generateDemoInsights();
    } catch (error) {
      console.error('Error loading category data:', error);
    }
  }

  generateDemoBusinesses() {
    const businesses = [
      {
        id: 1,
        name: "Ristorante Da Marco",
        subcategory: "Italian Restaurant",
        location: "Rome, Italy",
        rating: 4.8,
        reviews: 245,
        description: "Authentic Italian cuisine in the heart of Rome. Family recipes passed down through generations.",
        tags: ["Italian", "Family-owned", "Authentic", "Wine Selection"],
        price: "€€€",
        contact: {
          phone: "+39 06 123 4567",
          email: "info@damarco.it"
        }
      },
      {
        id: 2,
        name: "Le Petit Bistro",
        subcategory: "French Restaurant",
        location: "Paris, France",
        rating: 4.6,
        reviews: 189,
        description: "Classic French bistro offering traditional dishes with a modern twist.",
        tags: ["French", "Bistro", "Wine Bar", "Romantic"],
        price: "€€",
        contact: {
          phone: "+33 1 42 34 56 78",
          email: "contact@petitbistro.fr"
        }
      },
      {
        id: 3,
        name: "Tapas El Sol",
        subcategory: "Spanish Restaurant",
        location: "Barcelona, Spain",
        rating: 4.7,
        reviews: 312,
        description: "Traditional Spanish tapas bar with live flamenco shows every Friday.",
        tags: ["Spanish", "Tapas", "Live Music", "Sangria"],
        price: "€€",
        contact: {
          phone: "+34 93 123 4567",
          email: "hola@tapaselsol.es"
        }
      },
      {
        id: 4,
        name: "Biergarten München",
        subcategory: "German Restaurant",
        location: "Munich, Germany",
        rating: 4.5,
        reviews: 198,
        description: "Traditional Bavarian beer garden with authentic German cuisine and fresh beer.",
        tags: ["German", "Beer Garden", "Traditional", "Outdoor Seating"],
        price: "€€",
        contact: {
          phone: "+49 89 123 4567",
          email: "info@biergarten-muenchen.de"
        }
      },
      {
        id: 5,
        name: "Café Central",
        subcategory: "Coffee Shop",
        location: "Vienna, Austria",
        rating: 4.4,
        reviews: 156,
        description: "Historic Viennese coffee house serving the finest coffee and pastries since 1876.",
        tags: ["Coffee", "Historic", "Pastries", "WiFi"],
        price: "€",
        contact: {
          phone: "+43 1 123 4567",
          email: "info@cafecentral.at"
        }
      }
    ];
    return businesses;
  }

  generateDemoSubcategories() {
    const subcategoryData = {
      restaurants: [
        { 
          name: "Italian Restaurants", 
          count: 1250, 
          icon: "🍝",
          description: "Authentic Italian dining experiences across Europe",
          countries: 27,
          avgRating: 4.6
        },
        { 
          name: "French Restaurants", 
          count: 890, 
          icon: "🥖",
          description: "Classic French cuisine and bistro experiences",
          countries: 23,
          avgRating: 4.5
        },
        { 
          name: "Spanish Restaurants", 
          count: 720, 
          icon: "🥘",
          description: "Traditional Spanish and tapas restaurants",
          countries: 25,
          avgRating: 4.4
        },
        { 
          name: "German Restaurants", 
          count: 650, 
          icon: "🍺",
          description: "Bavarian and German traditional cuisine",
          countries: 18,
          avgRating: 4.3
        },
        { 
          name: "Coffee Shops", 
          count: 2100, 
          icon: "☕",
          description: "Cozy coffee shops and cafes",
          countries: 27,
          avgRating: 4.2
        },
        { 
          name: "Fast Food", 
          count: 1800, 
          icon: "🍔",
          description: "Quick service and fast food chains",
          countries: 27,
          avgRating: 3.8
        }
      ],
      technology: [
        { 
          name: "Software Development", 
          count: 3200, 
          icon: "💻",
          description: "Custom software development services",
          countries: 27,
          avgRating: 4.7
        },
        { 
          name: "Web Design", 
          count: 2800, 
          icon: "🎨",
          description: "Professional web design and UX services",
          countries: 27,
          avgRating: 4.6
        },
        { 
          name: "IT Support", 
          count: 2100, 
          icon: "🔧",
          description: "Technical support and IT services",
          countries: 27,
          avgRating: 4.4
        }
      ]
    };

    return subcategoryData[this.currentCategory] || subcategoryData.restaurants;
  }

  generateDemoCountries() {
    return [
      { name: "Germany", code: "DE", count: 45, flag: "assets/flags/de.png" },
      { name: "France", code: "FR", count: 38, flag: "assets/flags/fr.png" },
      { name: "Italy", code: "IT", count: 34, flag: "assets/flags/it.png" },
      { name: "Spain", code: "ES", count: 32, flag: "assets/flags/es.png" },
      { name: "Poland", code: "PL", count: 28, flag: "assets/flags/pl.png" },
      { name: "Netherlands", code: "NL", count: 25, flag: "assets/flags/nl.png" },
      { name: "Austria", code: "AT", count: 22, flag: "assets/flags/at.png" },
      { name: "Belgium", code: "BE", count: 20, flag: "assets/flags/be.png" }
    ];
  }

  generateDemoCities() {
    return [
      { name: "Paris", country: "France", count: 128 },
      { name: "Berlin", country: "Germany", count: 115 },
      { name: "Rome", country: "Italy", count: 98 },
      { name: "Madrid", country: "Spain", count: 87 },
      { name: "Amsterdam", country: "Netherlands", count: 76 },
      { name: "Vienna", country: "Austria", count: 65 },
      { name: "Barcelona", country: "Spain", count: 62 },
      { name: "Brussels", country: "Belgium", count: 58 }
    ];
  }

  generateDemoInsights() {
    const insightData = {
      restaurants: [
        {
          icon: "📈",
          title: "Market Growth",
          value: "+12%",
          label: "Year over Year",
          description: "Restaurant listings have grown by 12% this year"
        },
        {
          icon: "⭐",
          title: "Average Rating",
          value: "4.3",
          label: "Out of 5 Stars",
          description: "High customer satisfaction across all restaurants"
        },
        {
          icon: "💰",
          title: "Price Range",
          value: "€15-35",
          label: "Average Meal",
          description: "Competitive pricing across European markets"
        },
        {
          icon: "🌍",
          title: "Coverage",
          value: "27",
          label: "EU Countries",
          description: "Complete coverage across all European Union countries"
        }
      ]
    };

    return insightData[this.currentCategory] || insightData.restaurants;
  }

  setupEventListeners() {
    // Search functionality
    const searchButton = document.querySelector('.search-btn');
    if (searchButton) {
      searchButton.addEventListener('click', this.handleSearch.bind(this));
    }

    // Filter buttons
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(btn => {
      btn.addEventListener('click', (e) => this.handleFilter(e.target.dataset.filter));
    });

    // Breadcrumb navigation
    this.setupBreadcrumbs();
  }

  setupBreadcrumbs() {
    const categoriesLink = document.getElementById('categories-link');
    if (categoriesLink) {
      categoriesLink.href = `index.html#categories`;
    }
  }

  populatePage() {
    this.updatePageTitle();
    this.populateHeader();
    this.populateSubcategories();
    this.populateCountries();
    this.populateBusinesses();
    this.populateCities();
    this.populateInsights();
    this.populateRelatedCategories();
  }

  updatePageTitle() {
    const categoryName = this.formatCategoryName(this.currentCategory);
    document.title = `${categoryName} - Business Directory | ListAcross EU`;
    
    // Update breadcrumb
    const currentCategory = document.getElementById('current-category');
    if (currentCategory) {
      currentCategory.textContent = categoryName;
    }
  }

  populateHeader() {
    const categoryName = this.formatCategoryName(this.currentCategory);
    
    // Update title
    const titleElement = document.getElementById('category-title');
    if (titleElement) {
      titleElement.textContent = categoryName;
    }

    // Update tagline
    const taglineElement = document.getElementById('category-tagline');
    if (taglineElement) {
      const taglines = {
        restaurants: "Discover exceptional dining experiences across Europe",
        technology: "Connect with leading tech professionals and services",
        healthcare: "Find trusted healthcare providers in your area",
        education: "Explore educational institutions and services"
      };
      taglineElement.textContent = taglines[this.currentCategory] || taglines.restaurants;
    }

    // Update meta statistics
    this.updateMetaStats();
  }

  updateMetaStats() {
    const totalBusinesses = this.businesses.length * 200; // Simulate larger dataset
    const avgRating = (this.businesses.reduce((sum, b) => sum + b.rating, 0) / this.businesses.length).toFixed(1);
    
    document.getElementById('total-businesses').textContent = totalBusinesses.toLocaleString();
    document.getElementById('countries-covered').textContent = this.countries.length;
    document.getElementById('avg-rating').textContent = avgRating;
    document.getElementById('categories-count').textContent = this.subcategories.length;
  }

  populateSubcategories() {
    const container = document.getElementById('subcategories-container');
    if (!container) return;

    container.innerHTML = this.subcategories.map(sub => `
      <div class="subcategory-card" onclick="navigateToSubcategory('${sub.name}')">
        <span class="subcategory-icon">${sub.icon}</span>
        <h3>${sub.name}</h3>
        <p>${sub.description}</p>
        <div class="subcategory-stats">
          <div class="stat-item">
            <span class="stat-number">${sub.count}</span>
            <span class="stat-label">Businesses</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">${sub.countries}</span>
            <span class="stat-label">Countries</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">${sub.avgRating}</span>
            <span class="stat-label">Rating</span>
          </div>
        </div>
      </div>
    `).join('');
  }

  populateCountries() {
    const container = document.getElementById('countries-container');
    if (!container) return;

    container.innerHTML = this.countries.map(country => `
      <div class="country-item" onclick="navigateToCountry('${country.code}')">
        <img src="${country.flag}" alt="${country.name}" class="country-flag">
        <div class="country-info">
          <h4>${country.name}</h4>
          <span>${country.count} businesses</span>
        </div>
      </div>
    `).join('');
  }

  populateBusinesses() {
    const container = document.getElementById('businesses-container');
    if (!container) return;

    container.innerHTML = this.businesses.map(business => `
      <div class="business-card-category" onclick="navigateToBusiness(${business.id})">
        <div class="business-header-category">
          <h3>${business.name}</h3>
          <div class="business-location">📍 ${business.location}</div>
          <div class="business-rating">
            <span class="stars">${'⭐'.repeat(Math.floor(business.rating))}</span>
            <span class="rating-text">${business.rating} (${business.reviews} reviews)</span>
          </div>
        </div>
        <div class="business-details-category">
          <p>${business.description}</p>
          <div class="business-tags">
            ${business.tags.map(tag => `<span class="business-tag">${tag}</span>`).join('')}
          </div>
          <div class="business-contact">
            <div class="contact-info">
              <div>${business.price}</div>
              <div>${business.subcategory}</div>
            </div>
            <button class="btn-secondary">View Details</button>
          </div>
        </div>
      </div>
    `).join('');
  }

  populateCities() {
    const container = document.getElementById('cities-container');
    if (!container) return;

    container.innerHTML = this.cities.map(city => `
      <div class="city-card" onclick="navigateToCity('${city.name}')">
        <h4>${city.name}</h4>
        <div class="country-name">${city.country}</div>
        <div class="city-stats">${city.count} businesses</div>
      </div>
    `).join('');
  }

  populateInsights() {
    const container = document.getElementById('insights-container');
    if (!container) return;

    container.innerHTML = this.insights.map(insight => `
      <div class="insight-card">
        <span class="insight-icon">${insight.icon}</span>
        <h4>${insight.title}</h4>
        <div class="insight-value">${insight.value}</div>
        <div class="insight-label">${insight.label}</div>
      </div>
    `).join('');
  }

  populateRelatedCategories() {
    const container = document.getElementById('related-container');
    if (!container) return;

    const relatedCategories = [
      { name: "Hotels", count: "2.1k" },
      { name: "Entertainment", count: "1.8k" },
      { name: "Shopping", count: "3.2k" },
      { name: "Services", count: "2.7k" }
    ];

    container.innerHTML = relatedCategories.map(category => `
      <div class="related-card" onclick="navigateToCategory('${category.name.toLowerCase()}')">
        <h4>${category.name}</h4>
        <div class="related-count">${category.count} businesses</div>
      </div>
    `).join('');
  }

  handleSearch() {
    const searchTerm = document.getElementById('category-search').value;
    if (searchTerm) {
      window.location.href = `search-results.html?q=${encodeURIComponent(searchTerm)}&category=${this.currentCategory}`;
    }
  }

  handleFilter(filter) {
    console.log('Applying filter:', filter);
    // Add filter logic here
  }

  formatCategoryName(category) {
    return category.charAt(0).toUpperCase() + category.slice(1);
  }
}

// Navigation functions
window.navigateToSubcategory = function(subcategory) {
  window.location.href = `subcategory.html?subcategory=${encodeURIComponent(subcategory)}`;
};

window.navigateToCountry = function(countryCode) {
  window.location.href = `country.html?country=${countryCode}`;
};

window.navigateToBusiness = function(businessId) {
  window.location.href = `business-listing.html?id=${businessId}`;
};

window.navigateToCity = function(cityName) {
  window.location.href = `city.html?city=${encodeURIComponent(cityName)}`;
};

window.navigateToCategory = function(categoryName) {
  window.location.href = `category.html?category=${categoryName.toLowerCase()}`;
};

window.scrollToResults = function() {
  document.querySelector('.businesses-section').scrollIntoView({ 
    behavior: 'smooth' 
  });
};

window.showFilters = function() {
  // Toggle advanced filters
  console.log('Showing advanced filters');
};

// Initialize the category page when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new CategoryPage();
});