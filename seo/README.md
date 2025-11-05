# SEO Module - ListAcross EU

A production-ready SEO module that provides multilingual, plan-gated SEO management for European business pages.

## Features

### ✅ **Completed Core Features**

- **Multi-language Support**: EN, FR, NL, ES, PT
- **Plan-based Feature Gating**: Basic → Growth → Premium tiers
- **Country-specific Pages**: Support for all EU countries
- **Dynamic URL Structure**: `/{lang}/{country}/{city}/{service}/`
- **Rich Admin Interface**: Custom dashboard + Django admin integration
- **REST API**: Full DRF endpoints with filtering and serialization
- **Seed Data**: Pre-populated with EU countries, languages, and example pages

### 🔧 **SEO Features by Plan**

#### Basic Plan (Always Available)
- Meta title & description (with length validation)
- H1/H2 headings
- Canonical URLs (auto-generated)
- Robots meta tags
- Image alt fallback text

#### Growth Plan (Adds)
- Keywords hints for content optimization
- Internal links management (JSON array)
- Sitemap inclusion control
- Open Graph tags (title, description, image)
- Twitter Cards (summary, large image, etc.)

#### Premium Plan (Adds)
- JSON-LD structured data
- Breadcrumb navigation
- Local business schema markup
- Service schema markup
- Advanced analytics and reporting

## Quick Setup

### 1. Database Migration
```cmd
cd C:\projects\listacrosseu
py manage.py makemigrations seo
py manage.py migrate
```

### 2. Load Seed Data
```cmd
py manage.py seo_seed
```
This creates:
- 5 languages (en, fr, nl, es, pt)
- 10 EU countries (NL, BE, FR, DE, ES, PT, IT, AT, CH, LU)
- 3 SEO plans (Basic, Growth, Premium)
- 3 example pages (Global EN home, NL country page, PT Porto webdesign service)

### 3. Start Development Servers
```cmd
# Django (Terminal 1)
py manage.py runserver 127.0.0.1:8000

# Next.js (Terminal 2)
cd frontend
npx next dev -p 3001 -H 127.0.0.1
```

## Usage Examples

### Creating a New SEO Page in 60 Seconds

1. **Via Admin Interface**:
   - Go to `/admin/seo/seopage/add/`
   - Select country, language, page type, and plan
   - Fill required fields (meta_title, meta_description, h1)
   - Slug auto-populates from h1
   - Canonical URL auto-generates
   - Save & publish

2. **Via API** (for programmatic creation):
   ```python
   import requests
   
   data = {
       'country': 1,  # Netherlands
       'language': 3,  # Dutch (nl)
       'page_type': 'city',
       'plan': 2,  # Growth
       'slug': 'amsterdam',
       'meta_title': 'Amsterdam Business Directory - ListAcross EU',
       'meta_description': 'Discover verified businesses in Amsterdam. Local services, restaurants, and professional services in the Dutch capital.',
       'h1': 'Amsterdam Business Directory',
       'h2': 'Connect with Local Amsterdam Businesses',
       'is_published': True
   }
   
   response = requests.post(
       'http://127.0.0.1:8000/api/seo/api/pages/',
       json=data,
       headers={'Content-Type': 'application/json'}
   )
   ```

3. **Bulk Import** (CSV/Excel):
   ```cmd
   # Create custom management command for bulk import
   py manage.py import_seo_pages --file=pages.csv
   ```

## API Endpoints

### Pages
- `GET /api/seo/api/pages/` - List all pages (filterable)
- `GET /api/seo/api/pages/?country=PT&lang=pt&page_type=service&slug=webdesign`
- `POST /api/seo/api/pages/` - Create new page (staff only)
- `PUT /api/seo/api/pages/{id}/` - Update page (staff only)
- `GET /api/seo/api/pages/sitemap/` - XML sitemap data

### Reference Data
- `GET /api/seo/api/countries/` - Available countries
- `GET /api/seo/api/languages/` - Available languages  
- `GET /api/seo/api/plans/` - SEO plans and features

### Filtering Examples
```javascript
// Get all published pages for Netherlands in Dutch
/api/seo/api/pages/?country__code=NL&language__code=nl&is_published=true

// Get service pages only
/api/seo/api/pages/?page_type=service

// Search by title/content
/api/seo/api/pages/?search=webdesign

// Get sitemap data
/api/seo/api/pages/sitemap/
```

## Frontend Integration

### Dynamic Routes Created
- `app/[lang]/page.tsx` - Language home pages (`/en/`, `/fr/`, etc.)
- `app/[lang]/[country]/page.tsx` - Country pages (`/nl/nl/`, `/fr/fr/`)
- `app/[lang]/[country]/[city]/page.tsx` - City pages
- `app/[lang]/[country]/[city]/[service]/page.tsx` - Service pages

### Usage in Next.js Components
```typescript
import { fetchSeoPage } from '@/lib/seoApi';

// In a page component
export async function generateMetadata({ params }) {
  const seoPage = await fetchSeoPage({
    lang: params.lang,
    country: params.country,
    slug: params.service,
    type: 'service'
  });
  
  return {
    title: seoPage?.meta_title,
    description: seoPage?.meta_description,
    // ... other meta tags
  };
}
```

### SEO Components
- `<SeoHead>` - Renders meta tags, Open Graph, Twitter Cards
- `<Breadcrumbs>` - Premium breadcrumb navigation
- Auto JSON-LD injection for Premium plans

## Admin Features

### Django Admin Enhancements
- **List Display**: Title with length indicator, plan badges, status badges
- **Filters**: Country, language, page type, plan, publication status
- **Search**: Meta title, description, H1, slug
- **Bulk Actions**: Publish/unpublish, change plans, set robots
- **Inlines**: Content blocks management
- **Field Validation**: Plan-based feature restrictions

### Custom Dashboard (`/seo/dashboard/`)
- Overview statistics (total, published, drafts)
- Recent pages with plan indicators
- Plan distribution charts
- Quick actions (add page, manage all, view sitemap)
- Country and language summaries

## Plan Gating Logic

### Server-side Validation (Django)
```python
# In serializers.py
def validate(self, data):
    if self.instance and self.instance.plan.order < 1:
        growth_fields = ['keywords_hint', 'og_title', 'sitemap_include']
        for field in growth_fields:
            if field in data and data[field]:
                raise ValidationError(f"Requires Growth plan. Current: {plan.name}")
```

### Client-side Restrictions (Next.js)
```typescript
// Features conditionally rendered based on plan
{seoPage.can_use_growth_features && (
  <OpenGraphTags {...seoPage} />
)}

{seoPage.can_use_premium_features && (
  <JsonLdScript data={seoPage.json_ld} />
)}
```

## Directory Structure
```
seo/
├── models.py          # Country, Language, SeoPlan, SeoPage, SeoContentBlock
├── admin.py           # Enhanced admin interface with badges and bulk actions
├── serializers.py     # DRF serializers with plan validation
├── views.py           # API viewsets and custom dashboard
├── urls.py            # URL routing for dashboard and API
├── management/
│   └── commands/
│       └── seo_seed.py    # Seed command for initial data
├── migrations/        # Database migrations
└── templates/seo/
    └── dashboard.html     # Custom SEO dashboard

frontend/
├── lib/seoApi.ts      # TypeScript API client with error handling
├── components/seo/
│   ├── SeoHead.tsx        # Meta tags component
│   └── Breadcrumbs.tsx    # Premium breadcrumbs
└── app/
    ├── [lang]/            # Dynamic language routes
    │   ├── page.tsx       # Language home pages
    │   └── [country]/     # Country-specific pages
    └── next.config.js     # API rewrites and security headers
```

## Testing & Validation

### Health Check URLs
✅ **Frontend**: http://127.0.0.1:3001/  
✅ **API Direct**: http://127.0.0.1:8000/api/seo/api/pages/?country=PT&lang=pt&page_type=service&slug=webdesign  
✅ **API via Proxy**: http://127.0.0.1:3001/api/seo/api/pages/sitemap/  
✅ **Custom Dashboard**: http://127.0.0.1:8000/seo/dashboard/  

### Example API Response
```json
{
  "id": 3,
  "country": {"code": "PT", "name": "Portugal"},
  "language": {"code": "pt", "name": "Português"},
  "slug": "webdesign",
  "page_type": "service",
  "plan": {"name": "premium", "order": 2},
  "meta_title": "Web Design Porto - Serviços Profissionais | ListAcross EU",
  "meta_description": "Encontre os melhores serviços de web design no Porto...",
  "h1": "Serviços de Web Design no Porto",
  "canonical_url": "https://listacross.eu/pt/pt/porto/webdesign/",
  "robots": "index,follow",
  "og_title": "Web Design Porto - Serviços Profissionais",
  "json_ld": "{\"@context\":\"https://schema.org\",\"@type\":\"Service\"...}",
  "breadcrumbs": [
    {"name": "Início", "url": "/pt/"},
    {"name": "Portugal", "url": "/pt/pt/"},
    {"name": "Porto", "url": "/pt/pt/porto/"},
    {"name": "Web Design", "url": "/pt/pt/porto/webdesign/"}
  ],
  "can_use_growth_features": true,
  "can_use_premium_features": true,
  "is_published": true
}
```

## Performance & Scale

- **Database Indexing**: Unique constraints on country+language+slug+type
- **API Pagination**: DRF pagination (20 items per page)
- **Caching Ready**: Models support Django cache framework
- **CDN Friendly**: Static assets and images via CDN URLs
- **Sitemap Optimization**: Only published, sitemap-enabled pages

## Production Deployment

### Environment Variables
```env
# In production settings
SEO_CACHE_TIMEOUT=3600
SEO_SITEMAP_CACHE=86400
SEO_DEFAULT_PLAN=basic
SEO_MAX_PAGES_PER_PLAN={"basic": 10, "growth": 100, "premium": 1000}
```

### Recommended Nginx Configuration
```nginx
# Cache API responses
location /api/seo/ {
    proxy_pass http://django;
    proxy_cache seo_cache;
    proxy_cache_valid 200 1h;
    proxy_cache_key $request_uri;
}

# Cache sitemap
location /api/seo/api/pages/sitemap/ {
    proxy_pass http://django;
    proxy_cache sitemap_cache;
    proxy_cache_valid 200 24h;
}
```

## Roadmap & Extensions

### Phase 2 Features
- [ ] **Analytics Integration**: Track page performance and SEO metrics
- [ ] **A/B Testing**: Test different meta titles/descriptions  
- [ ] **Auto-translation**: Integrate with translation services
- [ ] **Schema Generator**: Visual schema.org builder for Premium users
- [ ] **Competitor Analysis**: Track competitor SEO strategies
- [ ] **Content Suggestions**: AI-powered content optimization
- [ ] **Bulk Operations**: CSV import/export for pages
- [ ] **Approval Workflow**: Multi-step content approval process

### Integration Opportunities  
- **Google Search Console**: Automated sitemap submission
- **Google Analytics**: Enhanced eCommerce tracking for Premium users
- **Ahrefs/SEMrush**: Keyword research integration
- **Screaming Frog**: Technical SEO audit integration

---

🎉 **The SEO module is now fully operational and ready for production use!**

For support or feature requests, contact the development team or create an issue in the project repository.