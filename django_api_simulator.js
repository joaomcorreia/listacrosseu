const express = require('express');
const cors = require('cors');

const app = express();
const PORT = 8000;

// Enable CORS for the Next.js frontend
app.use(cors({
  origin: ['http://localhost:3000', 'http://127.0.0.1:3000'],
  credentials: true
}));

app.use(express.json());

// Mock business data that matches Django's BusinessSerializer format
const mockBusinesses = [
  {
    id: 1,
    name: "Café Central Paris",
    description: "Traditional European coffee house with authentic pastries and specialty coffee blends. Experience the charm of old-world Paris.",
    localized_description: "Traditional European coffee house with authentic pastries and specialty coffee blends. Experience the charm of old-world Paris.",
    category: {
      id: 1,
      name: "Restaurant",
      localized_name: "Restaurant",
      slug: "restaurant"
    },
    owner_name: "Marie Dubois",
    email: "info@cafe-central.fr",
    phone: "+33 1 42 60 34 12",
    website: "https://cafe-central.fr",
    address: "123 Rue de la Paix",
    city: "Paris", 
    country: "France",
    postal_code: "75001",
    is_active: true,
    is_featured: true,
    is_verified: true,
    slug: "cafe-central-paris",
    images: [],
    created_at: "2023-01-15T10:30:00Z",
    updated_at: "2024-11-01T15:45:00Z"
  },
  {
    id: 2,
    name: "Tech Solutions Amsterdam",
    description: "Leading IT consulting firm specializing in cloud infrastructure, digital transformation, and enterprise software solutions.",
    localized_description: "Leading IT consulting firm specializing in cloud infrastructure, digital transformation, and enterprise software solutions.",
    category: {
      id: 2,
      name: "Technology",
      localized_name: "Technology", 
      slug: "technology"
    },
    owner_name: "Jan van der Berg",
    email: "contact@techsolutions.nl",
    phone: "+31 20 123 4567",
    website: "https://techsolutions.nl",
    address: "456 Herengracht",
    city: "Amsterdam",
    country: "Netherlands",
    postal_code: "1017 BZ",
    is_active: true,
    is_featured: false,
    is_verified: true,
    slug: "tech-solutions-amsterdam",
    images: [],
    created_at: "2023-02-20T14:15:00Z",
    updated_at: "2024-10-30T09:20:00Z"
  },
  {
    id: 3,
    name: "Flor de Lisboa",
    description: "Beautiful flower shop with fresh arrangements, wedding decorations, and event planning services since 1985.",
    localized_description: "Beautiful flower shop with fresh arrangements, wedding decorations, and event planning services since 1985.",
    category: {
      id: 3,
      name: "Retail",
      localized_name: "Retail",
      slug: "retail"
    },
    owner_name: "Ana Silva",
    email: "flores@flordelisboa.pt",
    phone: "+351 21 342 1567", 
    website: "https://flordelisboa.pt",
    address: "789 Rua Augusta",
    city: "Lisbon",
    country: "Portugal",
    postal_code: "1100-048",
    is_active: true,
    is_featured: false,
    is_verified: false,
    slug: "flor-de-lisboa",
    images: [],
    created_at: "2023-03-10T11:00:00Z",
    updated_at: "2024-11-02T16:30:00Z"
  },
  {
    id: 4,
    name: "Berlin Bakery",
    description: "Artisan bakery serving traditional German breads, pastries, and seasonal specialties made with organic ingredients.",
    localized_description: "Artisan bakery serving traditional German breads, pastries, and seasonal specialties made with organic ingredients.",
    category: {
      id: 1,
      name: "Restaurant",
      localized_name: "Restaurant",
      slug: "restaurant"
    },
    owner_name: "Hans Mueller",
    email: "info@berlinbakery.de",
    phone: "+49 30 987 6543",
    website: "https://berlinbakery.de",
    address: "321 Unter den Linden",
    city: "Berlin",
    country: "Germany", 
    postal_code: "10117",
    is_active: true,
    is_featured: true,
    is_verified: true,
    slug: "berlin-bakery",
    images: [],
    created_at: "2023-04-05T08:45:00Z",
    updated_at: "2024-11-03T12:15:00Z"
  },
  {
    id: 5,
    name: "Barcelona Design Studio",
    description: "Creative design agency specializing in branding, web design, and digital marketing for modern businesses.",
    localized_description: "Creative design agency specializing in branding, web design, and digital marketing for modern businesses.",
    category: {
      id: 4,
      name: "Design",
      localized_name: "Design",
      slug: "design"
    },
    owner_name: "Carlos Rodriguez",
    email: "hello@barcelonadesign.es", 
    phone: "+34 93 456 7890",
    website: "https://barcelonadesign.es",
    address: "654 Passeig de Gràcia",
    city: "Barcelona",
    country: "Spain",
    postal_code: "08008",
    is_active: true,
    is_featured: false,
    is_verified: true,
    slug: "barcelona-design-studio", 
    images: [],
    created_at: "2023-05-12T13:20:00Z",
    updated_at: "2024-11-04T10:40:00Z"
  },
  {
    id: 6,
    name: "Roma Pizzeria Autentica",
    description: "Family-owned pizzeria serving authentic Neapolitan pizza with imported ingredients and traditional wood-fired ovens.",
    localized_description: "Family-owned pizzeria serving authentic Neapolitan pizza with imported ingredients and traditional wood-fired ovens.",
    category: {
      id: 1,
      name: "Restaurant", 
      localized_name: "Restaurant",
      slug: "restaurant"
    },
    owner_name: "Giuseppe Romano",
    email: "ciao@romapizza.it",
    phone: "+39 06 123 4567",
    website: "https://romapizza.it",
    address: "987 Via del Corso",
    city: "Rome",
    country: "Italy",
    postal_code: "00186",
    is_active: true,
    is_featured: true,
    is_verified: true,
    slug: "roma-pizzeria-autentica",
    images: [],
    created_at: "2023-06-18T17:30:00Z", 
    updated_at: "2024-11-04T14:25:00Z"
  }
];

// Django-compatible search endpoint: /api/v1/search/businesses/
app.get('/api/v1/search/businesses/', (req, res) => {
  const {
    q = '',
    country = '',
    city = '',
    category = '',
    limit = '20',
    offset = '0',
    lang = 'en'
  } = req.query;

  console.log(`[${new Date().toISOString()}] Search API called:`, {
    query: q,
    country,
    city, 
    category,
    limit,
    offset,
    lang
  });

  let filteredBusinesses = [...mockBusinesses];

  // Apply text search filter (case-insensitive)
  if (q && q.trim()) {
    const searchTerm = q.toLowerCase();
    filteredBusinesses = filteredBusinesses.filter(business => 
      business.name.toLowerCase().includes(searchTerm) ||
      business.description.toLowerCase().includes(searchTerm) ||
      business.address.toLowerCase().includes(searchTerm) ||
      business.city.toLowerCase().includes(searchTerm) ||
      business.category.name.toLowerCase().includes(searchTerm)
    );
  }

  // Apply country filter
  if (country && country.trim()) {
    filteredBusinesses = filteredBusinesses.filter(business =>
      business.country.toLowerCase() === country.toLowerCase()
    );
  }

  // Apply city filter  
  if (city && city.trim()) {
    filteredBusinesses = filteredBusinesses.filter(business =>
      business.city.toLowerCase() === city.toLowerCase()
    );
  }

  // Apply category filter
  if (category && category.trim()) {
    filteredBusinesses = filteredBusinesses.filter(business =>
      business.category.name.toLowerCase() === category.toLowerCase()
    );
  }

  const total = filteredBusinesses.length;
  const limitNum = parseInt(limit) || 20;
  const offsetNum = parseInt(offset) || 0;

  // Apply pagination
  const paginatedResults = filteredBusinesses.slice(offsetNum, offsetNum + limitNum);

  // Format response to match Django's BusinessSearchView
  const response = {
    total: total,
    results: paginatedResults,
    query: q,
    language: lang,
    limit: limitNum,
    offset: offsetNum,
    has_more: total > (offsetNum + limitNum)
  };

  res.json(response);
});

// Countries list endpoint: /api/v1/countries/
app.get('/api/v1/countries/', (req, res) => {
  const countries = {};
  
  mockBusinesses.forEach(business => {
    if (business.country && business.country.trim()) {
      countries[business.country] = (countries[business.country] || 0) + 1;
    }
  });

  const response = Object.keys(countries)
    .sort()
    .map(country => ({
      code: country,
      name: country,
      total: countries[country]
    }));

  console.log(`[${new Date().toISOString()}] Countries API called: ${response.length} countries`);
  res.json(response);
});

// Cities by country endpoint: /api/v1/countries/{country}/cities/
app.get('/api/v1/countries/:country/cities/', (req, res) => {
  const { country } = req.params;
  const cities = {};
  
  mockBusinesses
    .filter(business => business.country && business.country.toLowerCase() === country.toLowerCase())
    .forEach(business => {
      if (business.city && business.city.trim()) {
        cities[business.city] = (cities[business.city] || 0) + 1;
      }
    });

  const response = Object.keys(cities)
    .sort()
    .map(city => ({
      slug: city,
      name: city,
      total: cities[city]
    }));

  console.log(`[${new Date().toISOString()}] Cities API called for ${country}: ${response.length} cities`);
  res.json(response);
});

// Categories list endpoint: /api/v1/categories/
app.get('/api/v1/categories/', (req, res) => {
  const categories = {};
  
  mockBusinesses.forEach(business => {
    if (business.category && business.category.name && business.category.name.trim()) {
      const categoryName = business.category.name;
      categories[categoryName] = (categories[categoryName] || 0) + 1;
    }
  });

  const response = Object.keys(categories)
    .sort()
    .map(category => ({
      slug: category,
      name: category,
      total: categories[category]
    }));

  console.log(`[${new Date().toISOString()}] Categories API called: ${response.length} categories`);
  res.json(response);
});

// Filtered businesses endpoint: /api/v1/businesses/
app.get('/api/v1/businesses/', (req, res) => {
  const {
    country = '',
    city = '',
    category = '',
    limit = '50',
    offset = '0'
  } = req.query;

  let filteredBusinesses = mockBusinesses.filter(business => {
    let matches = true;
    
    if (country && business.country) {
      matches = matches && business.country.toLowerCase() === country.toLowerCase();
    }
    
    if (city && business.city) {
      matches = matches && business.city.toLowerCase() === city.toLowerCase();
    }
    
    if (category && business.category && business.category.name) {
      matches = matches && business.category.name.toLowerCase() === category.toLowerCase();
    }
    
    return matches;
  });

  const total = filteredBusinesses.length;
  const limitNum = parseInt(limit) || 50;
  const offsetNum = parseInt(offset) || 0;

  const paginatedResults = filteredBusinesses.slice(offsetNum, offsetNum + limitNum);

  const response = {
    total: total,
    results: paginatedResults,
    limit: limitNum,
    offset: offsetNum,
    has_more: total > (offsetNum + limitNum)
  };

  console.log(`[${new Date().toISOString()}] Businesses API called: ${total} total, ${paginatedResults.length} returned`);
  res.json(response);
});

// Health check endpoint
app.get('/api/v1/health/', (req, res) => {
  res.json({
    status: 'ok',
    message: 'Django API Simulator running',
    timestamp: new Date().toISOString(),
    businesses_count: mockBusinesses.length
  });
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 Django API Simulator running on http://localhost:${PORT}`);
  console.log(`📡 Search endpoint: http://localhost:${PORT}/api/v1/search/businesses/`);
  console.log(`🔍 Example: http://localhost:${PORT}/api/v1/search/businesses/?q=cafe&limit=3`);
  console.log(`💚 Health check: http://localhost:${PORT}/api/v1/health/`);
  console.log(`\n✨ Ready to serve ${mockBusinesses.length} businesses to Next.js frontend!`);
});

module.exports = app;