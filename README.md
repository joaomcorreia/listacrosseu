# 🇪🇺 ListAcrossEU - European Business Directory

A comprehensive business directory platform covering all 27 EU countries with advanced search, filtering, and multi-language support.

## 🌟 Latest Version Features (November 2025)

### ✨ **Core Features**
- 🏢 **6,331+ Businesses** across all EU countries
- 🌍 **6 Languages**: English, Spanish, French, German, Dutch, Portuguese
- 🔍 **Advanced Search & Filtering** with real-time results
- 📱 **Responsive Design** optimized for all devices
- ⚡ **High Performance** with pagination and optimized loading

### 🎯 **Enhanced User Experience**
- 🎪 **Interactive Business Cards** with modal overlays
- 🎬 **Hero Slideshow** with animated content transitions
- 📰 **Blog Section** with article slider and multi-language content
- 🎨 **EU-Themed Design** with glassmorphism and gradients
- 🏷️ **Dynamic Country Landing Pages** for all 27 EU countries

### 🔧 **Technical Excellence**
- ⚡ **Next.js 15.0.0** for frontend with server-side rendering
- 🐍 **Django 5.2.7** for robust backend API
- 🎨 **Tailwind CSS** for modern, responsive styling
- 📊 **SQLite Database** with efficient pagination
- 🔗 **RESTful API** with comprehensive business data

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ with virtual environment
- Node.js 18+ with npm
- Git for version control

### Backend Setup (Django)
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_categories
python manage.py runserver 0.0.0.0:8000
```

### Frontend Setup (Next.js)
```bash
cd frontend
npm install
npm run dev
```

### Access the Application
- **Frontend**: http://localhost:3000 (or next available port)
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/

## 📱 Application Structure

### Frontend (`/frontend`)
```
app/
├── [lang]/                    # Language-specific routes
│   ├── page.tsx              # Homepage with slideshow & blog
│   ├── businesses/           # Business listings with search
│   ├── country/[code]/       # Dynamic country pages
│   └── [localized-routes]/   # Translated route names
components/
├── BusinessCard.tsx          # Enhanced cards with modals
├── BusinessModal.tsx         # Detailed business overlay
├── BlogSlider.tsx           # Article carousel
├── HeroSlideshow.tsx        # Animated homepage hero
├── SearchBar.tsx            # Advanced search component
└── FilterSidebar.tsx        # Category/location filters
lib/
├── api.ts                   # API integration layer
├── i18n.ts                  # Multi-language support
└── translations/            # Language files (EN/ES/FR/DE/NL/PT)
```

### Backend (`/backend`)
```
listacrosseu/
├── settings.py              # Django configuration
├── urls.py                  # API routing
└── views.py                 # Business logic & endpoints
data/
└── businesses.csv           # Source business data (6,331 records)
```

## 🌍 Multi-Language Support

### Supported Languages
- 🇬🇧 **English (EN)** - Default language
- 🇪🇸 **Spanish (ES)** - Empresas & Categorías  
- 🇫🇷 **French (FR)** - Entreprises & Catégories
- 🇩🇪 **German (DE)** - Unternehmen & Kategorien
- 🇳🇱 **Dutch (NL)** - Bedrijven & Categorieën
- 🇵🇹 **Portuguese (PT)** - Empresas & Categorias

### Localized Routes
Each language has its own URL structure:
- `/en/businesses` → `/es/empresas` → `/fr/entreprises` → `/de/unternehmen` → `/nl/bedrijven`
- Dynamic country pages: `/en/country/ES` → `/es/pais/ES`
- Blog articles with localized content and formatting

## 🔍 API Endpoints

### Business Listings
```
GET /api/businesses/
Parameters:
- page: Page number (default: 1)
- page_size: Items per page (20-100, default: 20)
- search: Search term for name/description
- country: Filter by country code (ES, FR, DE, etc.)
- city: Filter by city name
- category: Filter by business category
```

### Categories
```
GET /api/categories/
Parameters:
- country: Filter categories by country
- lang: Language for localized category names
```

## 🤖 AI Assistant Configuration

### Environment Setup

The AI Assistant feature requires proper endpoint configuration:

#### Development Environment
Create `frontend/.env.local`:
```bash
NEXT_PUBLIC_ASSISTANT_API=http://localhost:8000/assistant/api/ask/
```

#### Production Environment
In production, remove or update the environment variable to use relative URLs:
```bash
# Production uses same-origin relative URLs
NEXT_PUBLIC_ASSISTANT_API=/assistant/api/ask/
```

### API Endpoint
```
POST /assistant/api/ask/
Content-Type: application/json
Body: { "message": "Your question here" }
Response: { "reply": "Assistant response", "status": "ok" }
```

### CORS Handling
- **Development**: Cross-origin requests from `localhost:3000` to `localhost:8000`
- **Production**: Same-origin requests (no CORS issues)
- The backend is configured to handle CORS automatically for development
- No CSRF tokens required for the assistant endpoint (temporarily csrf_exempt)

### Chat Features
- **Real-time messaging** with typing indicators
- **Error handling** with retry functionality  
- **Keyboard shortcuts**: Enter to send, Shift+Enter for new lines
- **Accessibility** with proper ARIA labels and live regions
- **Timeout protection** (20-second request timeout)
- **Development logging** for debugging (no PII logged)

## 🎨 Design System

### Color Palette
- **Primary**: EU Blue (#003d82) to Purple gradients
- **Secondary**: Amber (#f59e0b) for featured content
- **Success**: Green (#10b981) for blog/articles
- **Background**: White to subtle gray gradients

### Typography
- **Headings**: Bold, gradient text effects
- **Body**: Clean, readable sans-serif
- **Accents**: Emoji icons and modern badges

### Components
- **Glassmorphism**: Backdrop blur effects on modals
- **Gradients**: Multi-color backgrounds for sections
- **Animations**: Smooth transitions and hover effects
- **Cards**: Elevated designs with shadows and borders

## 🚀 Performance Optimizations

### Frontend
- **Server-Side Rendering** with Next.js for SEO
- **Image Optimization** with lazy loading
- **Code Splitting** for faster page loads
- **Responsive Images** for different screen sizes

### Backend
- **Pagination** to handle large datasets efficiently
- **Database Indexing** for fast search queries
- **API Caching** for frequently accessed data
- **Optimized SQL** queries with minimal database hits

## 📊 Data & Statistics

### Business Coverage
- **27 EU Countries** with comprehensive data
- **6,331 Total Businesses** across all sectors
- **Multiple Categories** from technology to hospitality
- **Real Contact Information** including addresses, phones, websites

### Platform Metrics
- **Multi-device Support** (mobile, tablet, desktop)
- **Fast Load Times** under 3 seconds
- **SEO Optimized** with proper meta tags and structure
- **Accessibility Compliant** with WCAG guidelines

## 🔮 Future Enhancements

### Planned Features
- [ ] **User Authentication** with business owner accounts
- [ ] **Reviews & Ratings** system for businesses
- [ ] **Advanced Analytics** dashboard for insights
- [ ] **Mobile App** for iOS and Android
- [ ] **AI-Powered Recommendations** for users
- [ ] **Business Verification** system for authenticity

### Technical Improvements
- [ ] **PostgreSQL Migration** for production scalability
- [ ] **Redis Caching** for improved performance
- [ ] **CDN Integration** for global content delivery
- [ ] **Docker Containerization** for easy deployment
- [ ] **CI/CD Pipeline** with automated testing

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines and feel free to submit issues and enhancement requests.

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team & Contact

**Developer**: João Correia  
**GitHub**: [@joaomcorreia](https://github.com/joaomcorreia)  
**Repository**: [listacrosseu](https://github.com/joaomcorreia/listacrosseu)

---

### 🎉 **Latest Update**: November 2025
- ✅ Modal system for business details
- ✅ Blog section with article slider  
- ✅ Enhanced business cards with animations
- ✅ Improved homepage with hero slideshow
- ✅ Multi-language blog content
- ✅ Performance optimizations and bug fixes

**Built with ❤️ for the European business community** 🇪🇺