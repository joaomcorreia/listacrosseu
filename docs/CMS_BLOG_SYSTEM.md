# ListAcrossEU - CMS & Blog System Documentation

## Overview
The CMS and Blog system provides comprehensive content management capabilities with full SEO controls, multi-language support, and JSON-LD structured data.

## Features

### CMS Pages
- **Multi-language Support**: EN, NL, FR, ES, PT, DE, IT
- **SEO Controls**: Meta titles, descriptions, canonical URLs, noindex/nofollow
- **Social Media**: Open Graph images and custom JSON-LD data
- **Template System**: Custom template keys for flexible page layouts
- **Publishing Control**: Draft/published workflow

### Blog System
- **Categories**: Organized blog categories with color coding
- **Multi-language Posts**: Same language support as CMS
- **Author Management**: Posts linked to user accounts
- **Related Posts**: Manual selection + automatic category-based suggestions
- **Featured Posts**: Homepage featuring capability
- **Rich Content**: Excerpts, featured images, full content
- **SEO Integration**: Full SEO mixin inheritance

## API Endpoints

### CMS Endpoints
```
GET /api/v1/cms/pages/                    # List all pages (filtered by lang)
GET /api/v1/cms/pages/{lang}/{slug}/      # Get specific page
```

**Query Parameters:**
- `lang`: Language code (default: "en")

### Blog Endpoints
```
GET /api/v1/blog/categories/              # List all categories
GET /api/v1/blog/posts/                   # List all posts (filtered by lang, category, featured)
GET /api/v1/blog/posts/{lang}/{slug}/     # Get specific post with related posts
GET /api/v1/blog/search/?q={query}       # Search posts
GET /api/v1/blog/featured/                # Get featured posts for homepage
```

**Query Parameters:**
- `lang`: Language code (default: "en")
- `category`: Category slug filter
- `featured`: "true" to get only featured posts
- `q`: Search query (searches title, excerpt, content)

## Database Models

### CMS Page Model
- `title`: Page title
- `slug`: URL slug (unique per language)
- `language`: Language code
- `content`: Page content (HTML)
- `template_key`: Custom template identifier
- `is_published`: Publishing status
- **SEO Fields**: All inherited from SeoFieldsMixin

### Blog Category Model
- `name`: Category name
- `slug`: URL slug (unique)
- `description`: Category description
- `color`: Hex color code for UI theming

### Blog Post Model
- `title`: Post title
- `slug`: URL slug (unique per language)
- `language`: Language code
- `author`: User (foreign key)
- `category`: Category (foreign key, nullable)
- `excerpt`: Brief description (300 chars)
- `content`: Full post content (HTML)
- `featured_image`: Image upload
- `is_published`: Publishing status
- `is_featured`: Featured on homepage
- `published_at`: Publication timestamp
- `related_posts`: Many-to-many self-relation
- **SEO Fields**: All inherited from SeoFieldsMixin

## SEO Features

### Automatic SEO Handling
- **Title Fallback**: `seo_title()` method uses meta_title or falls back to content title
- **Canonical URLs**: Automatic generation if not specified
- **JSON-LD**: Custom structured data support
- **Open Graph**: Social media optimization

### Related Posts Algorithm
1. First uses manually selected related posts
2. If less than limit (default 3), fills remaining with posts from same category
3. Excludes current post and already selected posts
4. Filters by language and published status

## Admin Interface

### CMS Admin Features
- **Organized Fieldsets**: Route, Content, SEO, System sections
- **Search & Filter**: By title, language, published status
- **Slug Prepopulation**: Automatic slug generation from title

### Blog Admin Features
- **Category Management**: Name, slug, color administration
- **Post Management**: Full content and SEO control
- **Related Posts**: Horizontal filter widget for easy selection
- **Author Assignment**: Automatic author assignment on creation
- **Publishing Workflow**: Date hierarchy and status filtering

## Frontend Integration

### API Response Structure

**Page Detail Response:**
```json
{
  "id": 1,
  "title": "About Us",
  "slug": "about-us",
  "language": "en",
  "content": "<p>Page content here...</p>",
  "template_key": "standard",
  "is_published": true,
  "created_at": "2024-10-31T19:30:00Z",
  "updated_at": "2024-10-31T19:35:00Z",
  "meta": {
    "title": "About Us - ListAcrossEU",
    "description": "Learn about our European business directory platform",
    "canonical_url": null,
    "noindex": false,
    "nofollow": false,
    "og_image": "/media/seo/about-og.jpg",
    "json_ld": {"@type": "Organization", "name": "ListAcrossEU"}
  }
}
```

**Post Detail Response:**
```json
{
  "id": 1,
  "title": "Welcome to Our Blog",
  "slug": "welcome-blog",
  "language": "en",
  "excerpt": "This is our first blog post introducing the platform...",
  "content": "<p>Full blog post content...</p>",
  "category": {
    "id": 1,
    "name": "Announcements",
    "slug": "announcements",
    "color": "#3B82F6"
  },
  "author_name": "John Doe",
  "featured_image_url": "/media/blog/images/welcome.jpg",
  "is_featured": true,
  "published_at": "2024-10-31T19:00:00Z",
  "related_posts": [
    {
      "id": 2,
      "title": "Getting Started Guide",
      "slug": "getting-started",
      "excerpt": "Learn how to use our platform..."
    }
  ],
  "meta": {
    "title": "Welcome to Our Blog - ListAcrossEU",
    "description": "This is our first blog post introducing the platform...",
    "og_image": "/media/blog/images/welcome.jpg"
  }
}
```

## Usage Examples

### Creating a CMS Page
1. Go to Django Admin → CMS → Pages
2. Click "Add Page"
3. Fill in title, content, language
4. Set SEO fields (meta title, description)
5. Choose template key if needed
6. Publish when ready

### Creating a Blog Post
1. Go to Django Admin → Blog → Posts
2. Click "Add Post" 
3. Fill in title, excerpt, content
4. Select category and upload featured image
5. Set related posts if desired
6. Configure SEO settings
7. Mark as featured for homepage (optional)
8. Publish when ready

### Frontend API Calls
```javascript
// Get featured posts for homepage
const featuredPosts = await fetch('/api/v1/blog/featured/?lang=en');

// Get specific page
const aboutPage = await fetch('/api/v1/cms/pages/en/about-us/');

// Search blog posts
const searchResults = await fetch('/api/v1/blog/search/?q=business&lang=en');

// Get category posts
const categoryPosts = await fetch('/api/v1/blog/posts/?category=announcements&lang=en');
```

## Next Steps

### Frontend Implementation
1. Create CMS page components in Next.js
2. Implement blog listing and detail pages
3. Add related posts card slider
4. Integrate SEO meta tags and JSON-LD
5. Add search functionality

### Content Strategy
1. Create initial CMS pages (About, Privacy, Terms)
2. Set up blog categories
3. Write initial blog posts
4. Configure SEO for all content
5. Plan multilingual content rollout

The CMS and Blog system is now fully functional and ready for content creation and frontend integration!