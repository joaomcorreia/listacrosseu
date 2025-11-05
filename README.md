# ListAcross EU - Multi-language Business Directory

A comprehensive Django-based business directory platform with multi-language support for European markets.

## Features

- **Multi-language Support**: English, French, Dutch, Portuguese, German, Spanish, and Arabic
- **User Language Preferences**: Configurable language settings for dashboard and website
- **Business Listings API**: RESTful API with Django REST Framework
- **SEO Optimized**: Multi-language sitemaps and SEO-friendly URLs
- **Admin Interface**: Comprehensive Django admin for content management

## Language Support

### Supported Languages
- English (en) - Default
- French (fr)
- Dutch (nl)
- Portuguese (pt)
- German (de)
- Spanish (es)
- Arabic (ar) - with RTL support

### User Language Preferences
Users can configure:
- Arabic support on dashboard only
- Arabic support on both dashboard and website
- Primary language preference for content

## API Endpoints

### Business Listings
- `GET /api/v1/businesses/` - List businesses with language support
- `GET /api/v1/businesses/{slug}/` - Business detail
- `GET /api/v1/businesses/search/` - Advanced search with language filtering
- `GET /api/v1/categories/` - List categories

### User Accounts
- `GET /accounts/profile/` - User profile with language preferences
- `POST /accounts/set-language/` - Update language preferences
- `GET /accounts/user/` - Current user details

### Language Switching
All API endpoints support `?lang=xx` parameter to override language.

## Apps Structure

### accounts
- User profile management
- Language preference settings
- Authentication and user management

### listings
- Business listings and categories
- Multi-language content support
- Image management

### pages
- Static pages with translations
- Content management system

### seo
- SEO optimization tools
- Multi-language sitemaps
- Meta tag management

### billing
- Subscription management (placeholder)
- Invoice system (placeholder)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Create superuser:
```bash
python manage.py createsuperuser
```

4. Generate translation files:
```bash
python manage.py makemessages -l fr
python manage.py makemessages -l nl
python manage.py makemessages -l pt
python manage.py makemessages -l de
python manage.py makemessages -l es
python manage.py makemessages -l ar
```

5. Compile translations:
```bash
python manage.py compilemessages
```

6. Run development server:
```bash
python manage.py runserver
```

## Configuration

### Language Settings
The application uses Django's internationalization framework with custom middleware for user-specific language preferences.

### API Language Handling
- URL parameter: `?lang=xx`
- User profile preferences
- Session/cookie storage
- Browser Accept-Language header

### RTL Support
Arabic language automatically enables right-to-left layout with appropriate CSS styling.

## Development

### Adding New Languages
1. Add language to `LANGUAGES` in settings.py
2. Update language models with new fields
3. Generate and translate message files
4. Update frontend language switcher

### Custom Translation Logic
The application includes custom middleware that activates languages based on:
- User profile settings
- Arabic dashboard/website preferences
- URL parameters and session data

## Deployment Considerations

- Set `DEBUG = False` for production
- Configure proper `ALLOWED_HOSTS`
- Set up database (PostgreSQL recommended)
- Configure static/media file serving
- Set up proper secret key management

## License

This project is configured for European market deployment with GDPR compliance considerations.