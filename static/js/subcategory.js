// Subcategory Page JavaScript
class SubcategoryPage {
  constructor() {
    this.currentSubcategory = this.getSubcategoryFromURL();
    this.parentCategory = this.getParentCategoryFromURL();
    this.specialists = [];
    this.serviceAreas = [];
    this.faqs = [];
    this.currentView = 'list';
    this.currentSort = 'rating';
    
    this.init();
  }

  async init() {
    await this.loadSubcategoryData();
    this.setupEventListeners();
    this.populatePage();
  }

  getSubcategoryFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('subcategory') || 'Italian Restaurants';
  }

  getParentCategoryFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('category') || 'restaurants';
  }

  async loadSubcategoryData() {
    try {
      // In a real application, this would be API calls
      this.specialists = this.generateDemoSpecialists();
      this.serviceAreas = this.generateDemoServiceAreas();
      this.faqs = this.generateDemoFAQs();
    } catch (error) {
      console.error('Error loading subcategory data:', error);
    }
  }

  generateDemoSpecialists() {
    return [
      {
        id: 1,
        name: "Giuseppe Rossi",
        specialization: "Traditional Italian Cuisine",
        location: "Rome, Italy",
        rating: 4.9,
        reviewCount: 127,
        description: "Master chef with 20+ years experience in authentic Italian cooking. Specialized in Roman cuisine and homemade pasta.",
        skills: ["Pasta Making", "Roman Cuisine", "Wine Pairing", "Catering"],
        priceRange: "€€€",
        verified: true,
        responseTime: "2 hours",
        completedProjects: 340
      },
      {
        id: 2,
        name: "Maria Benedetti",
        specialization: "Northern Italian Cuisine",
        location: "Milan, Italy",
        rating: 4.8,
        reviewCount: 89,
        description: "Expert in Northern Italian regional dishes with focus on risotto and polenta preparations.",
        skills: ["Risotto", "Polenta", "Lombardy Cuisine", "Private Dining"],
        priceRange: "€€€€",
        verified: true,
        responseTime: "1 hour",
        completedProjects: 156
      },
      {
        id: 3,
        name: "Antonio Ferrucci",
        specialization: "Sicilian Cuisine",
        location: "Palermo, Italy",
        rating: 4.7,
        reviewCount: 203,
        description: "Sicilian chef bringing authentic island flavors with focus on seafood and traditional sweets.",
        skills: ["Seafood", "Cannoli", "Arancini", "Mediterranean"],
        priceRange: "€€",
        verified: true,
        responseTime: "3 hours",
        completedProjects: 267
      },
      {
        id: 4,
        name: "Franco Albertini",
        specialization: "Tuscan Cuisine",
        location: "Florence, Italy",
        rating: 4.6,
        reviewCount: 145,
        description: "Traditional Tuscan cooking with emphasis on local ingredients and wine pairings.",
        skills: ["Tuscan Recipes", "Local Ingredients", "Wine Selection", "Cooking Classes"],
        priceRange: "€€€",
        verified: false,
        responseTime: "4 hours",
        completedProjects: 198
      },
      {
        id: 5,
        name: "Lucia Veneziani",
        specialization: "Venetian Cuisine",
        location: "Venice, Italy",
        rating: 4.5,
        reviewCount: 76,
        description: "Venetian cuisine specialist with expertise in lagoon seafood and cicchetti preparation.",
        skills: ["Venetian Seafood", "Cicchetti", "Prosecco Pairing", "Event Catering"],
        priceRange: "€€€",
        verified: true,
        responseTime: "2 hours",
        completedProjects: 134
      }
    ];
  }

  generateDemoServiceAreas() {
    return [
      { name: "Rome", count: 45 },
      { name: "Milan", count: 38 },
      { name: "Naples", count: 32 },
      { name: "Florence", count: 28 },
      { name: "Venice", count: 24 },
      { name: "Bologna", count: 22 },
      { name: "Palermo", count: 18 },
      { name: "Turin", count: 16 }
    ];
  }

  generateDemoFAQs() {
    return [
      {
        question: "How do I choose the right Italian restaurant specialist?",
        answer: "Look for specialists with relevant experience in the specific Italian regional cuisine you prefer. Check their ratings, reviews, and verify their credentials. Consider factors like location, price range, and specialization in dishes you want to learn or serve."
      },
      {
        question: "What should I expect from an Italian cuisine consultation?",
        answer: "A typical consultation includes menu planning, ingredient sourcing advice, cooking technique guidance, and wine pairing recommendations. Many specialists also offer hands-on cooking lessons and can help with restaurant setup."
      },
      {
        question: "Do Italian cuisine specialists offer cooking classes?",
        answer: "Yes, many of our listed specialists provide cooking classes ranging from basic pasta making to advanced regional cuisine techniques. Classes can be conducted in-person or virtually, depending on the specialist."
      },
      {
        question: "What is the typical cost for Italian cuisine services?",
        answer: "Costs vary based on the service type and specialist experience. Consultation rates typically range from €50-150 per hour, while cooking classes can range from €80-200 per session. Catering services are quoted based on event size and menu complexity."
      },
      {
        question: "Can I find specialists for specific Italian regional cuisines?",
        answer: "Absolutely! Our specialists cover various Italian regional cuisines including Tuscan, Sicilian, Venetian, Roman, and Northern Italian specialties. Use our filters to find specialists by regional expertise."
      }
    ];
  }

  setupEventListeners() {
    // View toggle buttons
    document.querySelectorAll('.view-btn').forEach(btn => {
      btn.addEventListener('click', (e) => this.handleViewChange(e.target.dataset.view));
    });

    // Sort dropdown
    const sortSelect = document.getElementById('sort-select');
    if (sortSelect) {
      sortSelect.addEventListener('change', (e) => this.handleSortChange(e.target.value));
    }

    // Filter functionality
    this.setupFilters();

    // FAQ toggles
    this.setupFAQs();

    // Breadcrumb navigation
    this.setupBreadcrumbs();
  }

  setupFilters() {
    const locationFilter = document.getElementById('location-filter');
    const specializationFilter = document.getElementById('specialization-filter');
    const priceFilter = document.getElementById('price-filter');

    // Populate filter options
    if (locationFilter) {
      const locations = [...new Set(this.specialists.map(s => s.location.split(', ')[1]))];
      locationFilter.innerHTML = '<option value="">All Europe</option>' +
        locations.map(loc => `<option value="${loc}">${loc}</option>`).join('');
    }

    if (specializationFilter) {
      const specializations = [...new Set(this.specialists.map(s => s.specialization))];
      specializationFilter.innerHTML = '<option value="">All Specializations</option>' +
        specializations.map(spec => `<option value="${spec}">${spec}</option>`).join('');
    }
  }

  setupFAQs() {
    // FAQ toggles will be set up when FAQs are populated
  }

  setupBreadcrumbs() {
    const categoriesLink = document.getElementById('categories-link');
    const parentCategoryLink = document.getElementById('parent-category-link');

    if (categoriesLink) {
      categoriesLink.href = 'index.html#categories';
    }

    if (parentCategoryLink) {
      parentCategoryLink.href = `category.html?category=${this.parentCategory}`;
      parentCategoryLink.textContent = this.formatCategoryName(this.parentCategory);
    }
  }

  populatePage() {
    this.updatePageTitle();
    this.populateHeader();
    this.populateSpecialists();
    this.populateServiceAreas();
    this.populateGuide();
    this.populateFAQs();
  }

  updatePageTitle() {
    document.title = `${this.currentSubcategory} - ${this.formatCategoryName(this.parentCategory)} | ListAcross EU`;
    
    // Update breadcrumb
    const currentSubcategory = document.getElementById('current-subcategory');
    if (currentSubcategory) {
      currentSubcategory.textContent = this.currentSubcategory;
    }
  }

  populateHeader() {
    // Update parent category badge
    const parentCategoryBadge = document.getElementById('parent-category-badge');
    if (parentCategoryBadge) {
      parentCategoryBadge.textContent = this.formatCategoryName(this.parentCategory);
    }

    // Update subcategory title
    const subcategoryTitle = document.getElementById('subcategory-title');
    if (subcategoryTitle) {
      subcategoryTitle.textContent = this.currentSubcategory;
    }

    // Update tagline
    const subcategoryTagline = document.getElementById('subcategory-tagline');
    if (subcategoryTagline) {
      const taglines = {
        "Italian Restaurants": "Authentic Italian dining experiences with traditional flavors",
        "French Restaurants": "Elegant French cuisine and bistro experiences",
        "Software Development": "Custom software solutions for your business needs",
        "Web Design": "Professional web design and user experience services"
      };
      subcategoryTagline.textContent = taglines[this.currentSubcategory] || "Professional services you can trust";
    }

    // Update meta statistics
    this.updateMetaStats();

    // Update description
    this.updateDescription();
  }

  updateMetaStats() {
    const totalSpecialists = this.specialists.length;
    const countries = [...new Set(this.specialists.map(s => s.location.split(', ')[1]))].length;
    const avgRating = (this.specialists.reduce((sum, s) => sum + s.rating, 0) / this.specialists.length).toFixed(1);
    const priceRange = this.calculatePriceRange();

    document.getElementById('total-specialists').textContent = totalSpecialists;
    document.getElementById('countries-served').textContent = countries;
    document.getElementById('avg-rating-display').textContent = avgRating;
    document.getElementById('price-range').textContent = priceRange;
  }

  updateDescription() {
    const subcategoryDescription = document.getElementById('subcategory-description');
    if (subcategoryDescription) {
      const descriptions = {
        "Italian Restaurants": "Discover authentic Italian restaurants across Europe, offering traditional recipes passed down through generations. From Northern Italian risottos to Sicilian seafood, find the perfect Italian dining experience near you.",
        "French Restaurants": "Experience the finest French cuisine from bistros to fine dining establishments. Our curated selection of French restaurants offers everything from classic dishes to modern interpretations of traditional French cooking.",
        "Software Development": "Connect with experienced software developers who can bring your ideas to life. Whether you need custom applications, web development, or mobile apps, find the right development partner for your project.",
        "Web Design": "Find talented web designers who create beautiful, functional websites that drive results. From e-commerce platforms to corporate websites, discover designers who understand your vision and business goals."
      };
      subcategoryDescription.textContent = descriptions[this.currentSubcategory] || "Find the best professionals in this category across Europe.";
    }
  }

  calculatePriceRange() {
    const prices = this.specialists.map(s => s.priceRange);
    const uniquePrices = [...new Set(prices)];
    if (uniquePrices.length === 1) return uniquePrices[0];
    return `${uniquePrices[0]}-${uniquePrices[uniquePrices.length - 1]}`;
  }

  populateSpecialists() {
    const container = document.getElementById('specialists-container');
    if (!container) return;

    // Apply current view class
    container.className = `specialists-container view-${this.currentView}`;

    const sortedSpecialists = this.sortSpecialists(this.specialists);

    container.innerHTML = sortedSpecialists.map(specialist => `
      <div class="specialist-card" onclick="contactSpecialist(${specialist.id})">
        <div class="specialist-header">
          ${specialist.verified ? '<div class="specialist-badge">✓ Verified</div>' : ''}
          <div class="specialist-name">${specialist.name}</div>
          <div class="specialist-specialization">${specialist.specialization}</div>
          <div class="specialist-location">📍 ${specialist.location}</div>
          <div class="specialist-rating">
            <span class="stars">${'⭐'.repeat(Math.floor(specialist.rating))}</span>
            <span class="rating-score">${specialist.rating}</span>
            <span class="rating-count">(${specialist.reviewCount} reviews)</span>
          </div>
        </div>
        <div class="specialist-details">
          <p class="specialist-description">${specialist.description}</p>
          <div class="specialist-skills">
            ${specialist.skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
          </div>
          <div class="specialist-footer">
            <div class="price-range">${specialist.priceRange}</div>
            <button class="contact-specialist" onclick="event.stopPropagation(); contactSpecialist(${specialist.id})">
              Contact Specialist
            </button>
          </div>
        </div>
      </div>
    `).join('');
  }

  populateServiceAreas() {
    const container = document.getElementById('service-areas-container');
    if (!container) return;

    container.innerHTML = this.serviceAreas.map(area => `
      <div class="service-area-card" onclick="navigateToCity('${area.name}')">
        <h4>${area.name}</h4>
        <div class="service-area-count">${area.count} specialists</div>
      </div>
    `).join('');
  }

  populateGuide() {
    // Update guide content based on subcategory
    const credentialsGuide = document.getElementById('credentials-guide');
    const reviewsGuide = document.getElementById('reviews-guide');
    const pricingGuide = document.getElementById('pricing-guide');
    const experienceGuide = document.getElementById('experience-guide');

    if (credentialsGuide) {
      const credentialTips = {
        "Italian Restaurants": "Look for culinary certifications, Italian cooking credentials, and professional kitchen experience.",
        "Software Development": "Check for relevant programming certifications, computer science degrees, and portfolio of completed projects.",
        "Web Design": "Verify design certifications, UX/UI credentials, and a strong portfolio of previous work."
      };
      credentialsGuide.textContent = credentialTips[this.currentSubcategory] || "Look for relevant certifications and professional qualifications.";
    }
  }

  populateFAQs() {
    const container = document.getElementById('faq-container');
    if (!container) return;

    container.innerHTML = this.faqs.map((faq, index) => `
      <div class="faq-item" data-index="${index}">
        <div class="faq-question" onclick="toggleFAQ(${index})">
          ${faq.question}
          <span class="faq-toggle">+</span>
        </div>
        <div class="faq-answer">
          <p>${faq.answer}</p>
        </div>
      </div>
    `).join('');
  }

  handleViewChange(view) {
    this.currentView = view;
    
    // Update button states
    document.querySelectorAll('.view-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.view === view);
    });

    // Re-populate specialists with new view
    this.populateSpecialists();
  }

  handleSortChange(sortBy) {
    this.currentSort = sortBy;
    this.populateSpecialists();
  }

  sortSpecialists(specialists) {
    return [...specialists].sort((a, b) => {
      switch (this.currentSort) {
        case 'rating':
          return b.rating - a.rating;
        case 'reviews':
          return b.reviewCount - a.reviewCount;
        case 'price':
          return this.comparePriceRange(a.priceRange, b.priceRange);
        case 'price-desc':
          return this.comparePriceRange(b.priceRange, a.priceRange);
        case 'newest':
          return b.id - a.id; // Assuming higher ID means newer
        default:
          return 0;
      }
    });
  }

  comparePriceRange(a, b) {
    const priceValues = { '€': 1, '€€': 2, '€€€': 3, '€€€€': 4 };
    return priceValues[a] - priceValues[b];
  }

  formatCategoryName(category) {
    return category.charAt(0).toUpperCase() + category.slice(1);
  }
}

// Global functions
window.contactSpecialist = function(specialistId) {
  console.log('Contacting specialist:', specialistId);
  // In a real app, this would open a contact modal or navigate to contact page
  alert('Contact functionality would be implemented here');
};

window.navigateToCity = function(cityName) {
  window.location.href = `city.html?city=${encodeURIComponent(cityName)}`;
};

window.toggleFAQ = function(index) {
  const faqItem = document.querySelector(`[data-index="${index}"]`);
  if (faqItem) {
    faqItem.classList.toggle('active');
  }
};

window.applyQuickFilters = function() {
  const locationFilter = document.getElementById('location-filter').value;
  const specializationFilter = document.getElementById('specialization-filter').value;
  const priceFilter = document.getElementById('price-filter').value;

  console.log('Applying filters:', { locationFilter, specializationFilter, priceFilter });
  // Implement filtering logic here
};

window.showFilters = function() {
  console.log('Showing advanced filters');
  // Implement advanced filters modal/panel
};

window.scrollToResults = function() {
  document.querySelector('.specialists-section').scrollIntoView({ 
    behavior: 'smooth' 
  });
};

// Initialize the subcategory page when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new SubcategoryPage();
});