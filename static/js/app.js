// Configuration
const API_BASE_URL = 'http://localhost:3001/api';

// Enhanced flags slider with click navigation
function initializeEnhancedFlagSlider() {
  const track = document.querySelector('.flags .track, #flag-track');
  if (!track || window.flagSliderInitialized) return;

  let speed = 0.8; // px per frame
  let pos = 0;
  let isPaused = false;
  let animationId;

  function setupClones() {
    // duplicate items to enable infinite loop
    const items = Array.from(track.children);
    items.forEach(item => {
      const clone = item.cloneNode(true);
      // Preserve click handlers for clones
      if (item.href) clone.href = item.href;
      if (item.dataset.country) clone.dataset.country = item.dataset.country;
      track.appendChild(clone);
    });
  }

  function loop() {
    if (!isPaused) {
      pos -= speed;
      if (Math.abs(pos) >= track.scrollWidth / 2) {
        pos = 0;
      }
      track.style.transform = `translateX(${pos}px)`;
    }
    animationId = requestAnimationFrame(loop);
  }

  // Setup hover pause functionality
  const flagsSection = document.querySelector('.flags');
  if (flagsSection) {
    flagsSection.addEventListener('mouseenter', () => {
      isPaused = true;
    });
    flagsSection.addEventListener('mouseleave', () => {
      isPaused = false;
    });
  }

  // Remove conflicting click handlers - let flag_slider.html handle navigation

  // Initialize
  setupClones();
  requestAnimationFrame(loop);
  window.flagSliderInitialized = true;

  return {
    pause: () => isPaused = true,
    resume: () => isPaused = false,
    destroy: () => {
      if (animationId) cancelAnimationFrame(animationId);
      window.flagSliderInitialized = false;
    }
  };
}

// Auto-initialize on DOM ready
document.addEventListener('DOMContentLoaded', function () {
  // Check if we're using the new flag slider template
  if (document.querySelector('#flag-track')) {
    // New template will handle its own initialization
    return;
  }

  // Initialize legacy flag slider if present
  const track = document.querySelector('.flags .track');
  if (track && !window.flagSliderInitialized) {
    window.flagSlider = initializeEnhancedFlagSlider();
  }
});

// Featured Cards Slider
const featuredTrack = document.querySelector('.featured-track');
const featuredCards = document.querySelectorAll('.featured-card');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');
const dotsContainer = document.querySelector('.slider-dots');

if (featuredTrack && featuredCards.length > 0) {
  let currentIndex = 0;
  const cardsToShow = 3; // Number of cards visible at once
  const totalSlides = Math.ceil(featuredCards.length / cardsToShow);

  // Create dots
  for (let i = 0; i < totalSlides; i++) {
    const dot = document.createElement('div');
    dot.className = 'slider-dot';
    if (i === 0) dot.classList.add('active');
    dot.addEventListener('click', () => goToSlide(i));
    dotsContainer.appendChild(dot);
  }

  const dots = document.querySelectorAll('.slider-dot');

  function updateSlider() {
    const cardWidth = 320 + 24; // card width + gap
    const translateX = -(currentIndex * cardsToShow * cardWidth);
    featuredTrack.style.transform = `translateX(${translateX}px)`;

    // Update dots
    dots.forEach((dot, index) => {
      dot.classList.toggle('active', index === currentIndex);
    });
  }

  function goToSlide(index) {
    currentIndex = index;
    updateSlider();
  }

  function nextSlide() {
    currentIndex = (currentIndex + 1) % totalSlides;
    updateSlider();
  }

  function prevSlide() {
    currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
    updateSlider();
  }

  // Button event listeners
  if (nextBtn) nextBtn.addEventListener('click', nextSlide);
  if (prevBtn) prevBtn.addEventListener('click', prevSlide);

  // Card click handlers
  featuredCards.forEach(card => {
    card.addEventListener('click', () => {
      const location = card.dataset.location;
      if (location) {
        // Parse location format: "city-countrycode"
        const parts = location.split('-');
        if (parts.length === 2) {
          const cityName = parts[0].charAt(0).toUpperCase() + parts[0].slice(1);
          window.location.href = `/city/${cityName}/`;
        }
      }
    });
  });

  // Auto-slide every 5 seconds
  setInterval(nextSlide, 5000);

  // Pause auto-slide on hover
  featuredTrack.addEventListener('mouseenter', () => clearInterval());
  featuredTrack.addEventListener('mouseleave', () => setInterval(nextSlide, 5000));
}

// Business Categories Cards
const categoryCards = document.querySelectorAll('.category-card');
const seeAllButtons = document.querySelectorAll('.see-all-btn');

if (categoryCards.length > 0) {
  categoryCards.forEach(card => {
    card.addEventListener('click', (e) => {
      // Don't trigger if clicking the "See All" button
      if (e.target.classList.contains('see-all-btn')) return;

      const category = card.dataset.category;
      if (category) {
        // Navigate to category page or search results
        window.location.href = `/search/?category=${category}`;
      }
    });
  });
}

if (seeAllButtons.length > 0) {
  seeAllButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      e.stopPropagation(); // Prevent card click
      const card = button.closest('.category-card');
      const category = card.dataset.category;

      if (category) {
        window.location.href = `/search/?category=${category}`;
      }
    });
  });
}

// Trending Destinations Cards
const trendingCards = document.querySelectorAll('.trending-card');
const exploreAllBtn = document.querySelector('.explore-all-btn');

if (trendingCards.length > 0) {
  trendingCards.forEach(card => {
    card.addEventListener('click', () => {
      const destination = card.dataset.destination;

      // For demo purposes, redirect to search with location
      if (destination) {
        // Extract city from destination format "city-country"
        const parts = destination.split('-');
        if (parts.length >= 1) {
          const searchQuery = parts[0].charAt(0).toUpperCase() + parts[0].slice(1);
          window.location.href = `/search/?q=${searchQuery}`;
        }
      }
    });

    // Add parallax effect on mouse move
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top) / rect.height) * 100;

      card.style.backgroundPosition = `${x}% ${y}%`;
    });

    card.addEventListener('mouseleave', () => {
      card.style.backgroundPosition = 'center';
    });
  });
}

if (exploreAllBtn) {
  exploreAllBtn.addEventListener('click', () => {
    window.location.href = '/search/';
  });
}

// API Functions
async function searchBusinesses(query, filters = {}) {
  try {
    const params = new URLSearchParams({
      q: query,
      ...filters
    });

    const response = await fetch(`${API_BASE_URL}/search?${params}`);
    const data = await response.json();
    return data.results || [];
  } catch (error) {
    console.error('Search error:', error);
    return [];
  }
}

async function getBusinessesByCountry(countryCode) {
  try {
    const response = await fetch(`${API_BASE_URL}/countries/${countryCode}/businesses`);
    const data = await response.json();
    return data.businesses || [];
  } catch (error) {
    console.error('Error fetching businesses by country:', error);
    return [];
  }
}

async function getBusinessStats() {
  try {
    const response = await fetch(`${API_BASE_URL}/stats`);
    return await response.json();
  } catch (error) {
    console.error('Error fetching stats:', error);
    return null;
  }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', async function () {
  // Initialize search functionality
  initializeSearch();

  // Load and update statistics
  await updateStatistics();

  // Add click handlers for country flags
  initializeCountryFlags();
});

function initializeSearch() {
  const searchForm = document.querySelector('.searchbar');
  const searchInput = searchForm.querySelector('input');
  const searchButton = searchForm.querySelector('button');

  // Handle search
  const handleSearch = async () => {
    const query = searchInput.value.trim();
    if (!query) return;

    // Show loading state
    searchButton.textContent = 'Searching...';
    searchButton.disabled = true;

    try {
      const results = await searchBusinesses(query);
      displaySearchResults(results, query);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      searchButton.textContent = 'Search';
      searchButton.disabled = false;
    }
  };

  searchButton.addEventListener('click', handleSearch);
  searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSearch();
    }
  });
}

function displaySearchResults(results, query) {
  // Create or update results container
  let resultsContainer = document.getElementById('search-results');
  if (!resultsContainer) {
    resultsContainer = document.createElement('div');
    resultsContainer.id = 'search-results';
    resultsContainer.className = 'search-results';

    // Insert after the map section
    const mapSection = document.querySelector('.map-wrap');
    mapSection.parentNode.insertBefore(resultsContainer, mapSection.nextSibling);
  }

  if (results.length === 0) {
    resultsContainer.innerHTML = `
      <div class="container">
        <div class="no-results">
          <h3>No results found for "${query}"</h3>
          <p>Try adjusting your search terms or browse by category below.</p>
        </div>
      </div>
    `;
    return;
  }

  resultsContainer.innerHTML = `
    <div class="container">
      <div class="results-header">
        <h2>Search Results for "${query}"</h2>
        <p>Found ${results.length} businesses</p>
      </div>
      <div class="results-grid">
        ${results.map(business => createBusinessCard(business)).join('')}
      </div>
    </div>
  `;
}

function createBusinessCard(business) {
  const truncateText = (text, maxLength) => {
    if (!text) return '';
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
  };

  return `
    <div class="business-card" onclick="window.location.href='business-listing.html?id=${business.id}'">
      <div class="business-header">
        <h3 class="business-name">${business.name}</h3>
        <span class="business-category">${business.category}</span>
      </div>
      <div class="business-location">
        📍 ${business.city}, ${business.country}
      </div>
      ${business.description ? `<p class="business-description">${truncateText(business.description, 120)}</p>` : ''}
      <div class="business-meta">
        ${business.phone ? `<span>📞 ${business.phone}</span>` : ''}
        ${business.website ? `<span>🌐 Website</span>` : ''}
      </div>
    </div>
  `;
}

async function updateStatistics() {
  try {
    const stats = await getBusinessStats();
    if (!stats) return;

    // Update category counts in the existing cards
    const cards = document.querySelectorAll('.card');

    // Update counts with real data when available
    if (stats.businessesByCategory) {
      stats.businessesByCategory.forEach((item, index) => {
        if (cards[index]) {
          const category = item.category;
          const count = item.count;

          // Update the card title if it matches
          const cardTitle = cards[index].querySelector('h3');
          if (cardTitle && cardTitle.textContent.toLowerCase().includes(category.toLowerCase())) {
            // Update the counts in the list items
            const listItems = cards[index].querySelectorAll('li strong');
            if (listItems.length > 0) {
              listItems[0].textContent = `(${count})`;
            }
          }
        }
      });
    }
  } catch (error) {
    console.error('Error updating statistics:', error);
  }
}

function initializeCountryFlags() {
  const flags = document.querySelectorAll('.flag-item');

  flags.forEach(flag => {
    // Only add hover effects, let the HTML href handle navigation
    flag.addEventListener('mouseenter', () => {
      flag.style.transform = 'scale(1.05)';
      flag.style.transition = 'transform 0.2s';
    });

    flag.addEventListener('mouseleave', () => {
      flag.style.transform = 'scale(1)';
    });
  });
}

function getCountryCode(countryName) {
  const countryMap = {
    'Austria': 'at',
    'Belgium': 'be',
    'Bulgaria': 'bg',
    'Croatia': 'hr',
    'Cyprus': 'cy',
    'Czechia': 'cz',
    'Denmark': 'dk',
    'Estonia': 'ee',
    'Finland': 'fi',
    'France': 'fr',
    'Germany': 'de',
    'Greece': 'gr',
    'Hungary': 'hu',
    'Ireland': 'ie',
    'Italy': 'it',
    'Latvia': 'lv',
    'Lithuania': 'lt',
    'Luxembourg': 'lu',
    'Malta': 'mt',
    'Netherlands': 'nl',
    'Poland': 'pl',
    'Portugal': 'pt',
    'Romania': 'ro',
    'Slovakia': 'sk',
    'Slovenia': 'si',
    'Spain': 'es',
    'Sweden': 'se'
  };

  return countryMap[countryName];
}

function getCountrySlug(countryName) {
  const slugMap = {
    'Austria': 'austria',
    'Belgium': 'belgium',
    'Bulgaria': 'bulgaria',
    'Croatia': 'croatia',
    'Cyprus': 'cyprus',
    'Czechia': 'czechia',
    'Denmark': 'denmark',
    'Estonia': 'estonia',
    'Finland': 'finland',
    'France': 'france',
    'Germany': 'germany',
    'Greece': 'greece',
    'Hungary': 'hungary',
    'Ireland': 'ireland',
    'Italy': 'italy',
    'Latvia': 'latvia',
    'Lithuania': 'lithuania',
    'Luxembourg': 'luxembourg',
    'Malta': 'malta',
    'Netherlands': 'netherlands',
    'Poland': 'poland',
    'Portugal': 'portugal',
    'Romania': 'romania',
    'Slovakia': 'slovakia',
    'Slovenia': 'slovenia',
    'Spain': 'spain',
    'Sweden': 'sweden'
  };

  return slugMap[countryName] || countryName.toLowerCase();
}

// Blog Posts Slider
document.addEventListener('DOMContentLoaded', function () {
  const blogSlider = document.querySelector('.blog-slider');
  const blogPrevBtn = document.querySelector('.blog-prev');
  const blogNextBtn = document.querySelector('.blog-next');

  if (blogSlider && blogPrevBtn && blogNextBtn) {
    const scrollAmount = 370; // Card width + gap

    function updateNavButtons() {
      const scrollLeft = blogSlider.scrollLeft;
      const maxScroll = blogSlider.scrollWidth - blogSlider.clientWidth;

      blogPrevBtn.disabled = scrollLeft <= 0;
      blogNextBtn.disabled = scrollLeft >= maxScroll - 1; // -1 for precision
    }

    blogPrevBtn.addEventListener('click', () => {
      blogSlider.scrollBy({
        left: -scrollAmount,
        behavior: 'smooth'
      });
    });

    blogNextBtn.addEventListener('click', () => {
      blogSlider.scrollBy({
        left: scrollAmount,
        behavior: 'smooth'
      });
    });

    blogSlider.addEventListener('scroll', updateNavButtons);

    // Initialize button states
    updateNavButtons();

    // Auto-scroll functionality (optional)
    let autoScrollInterval;

    function startAutoScroll() {
      autoScrollInterval = setInterval(() => {
        if (!blogNextBtn.disabled) {
          blogSlider.scrollBy({
            left: scrollAmount,
            behavior: 'smooth'
          });
        } else {
          // Reset to beginning
          blogSlider.scrollTo({
            left: 0,
            behavior: 'smooth'
          });
        }
      }, 5000); // Auto-scroll every 5 seconds
    }

    function stopAutoScroll() {
      clearInterval(autoScrollInterval);
    }

    // Pause auto-scroll on hover
    blogSlider.addEventListener('mouseenter', stopAutoScroll);
    blogSlider.addEventListener('mouseleave', startAutoScroll);

    // Start auto-scroll initially
    startAutoScroll();
  }
});