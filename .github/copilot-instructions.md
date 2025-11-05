# ListAcross EU - AI Coding Agent Instructions

## Architecture Overview

This is a **bilingual Django + Next.js** business directory platform targeting European markets. The backend is Django with DRF serving a Next.js frontend via API proxy.

**Key Components:**
- **Backend**: Django 4.2 with DRF, SQLite (dev), custom i18n middleware
- **Frontend**: Next.js 14 with TypeScript, Tailwind CSS, internationalized routing
- **Languages**: EN (default), FR, NL, PT, DE, ES, AR (with RTL + dashboard/website preferences)

## Critical Development Patterns

### Multi-Language Architecture
- **Django**: Uses individual `*_en`, `*_fr`, etc. fields per model (not django-modeltranslation)
- **Frontend**: Uses `[lang]` dynamic routing with middleware redirects, custom `i18n/ui.ts` translations
- **User Preferences**: `UserProfile` model with `arabic_on_dashboard` and `arabic_on_website` boolean flags
- **Custom Middleware**: `middleware/language.py` handles complex Arabic preference logic

### Development Workflow
```bash
# Backend (always run from project root)
python manage.py runserver 127.0.0.1:8000
python manage.py makemigrations && python manage.py migrate

# Frontend (cd to frontend/ directory first)
cd frontend && npm run dev  # localhost:3000
cd frontend && npm run build

# Translation updates
python manage.py makemessages -l fr -l nl -l pt -l de -l es -l ar
python manage.py compilemessages
```

### API Integration Patterns
- **CORS**: Configured for `localhost:3000` in Django settings
- **Proxy**: Next.js rewrites `/api/*` to `http://127.0.0.1:8000/api/*`
- **Endpoints**: Follow `/api/v1/` prefix with DRF ViewSets
- **Language Support**: All API endpoints accept `?lang=xx` parameter

### Database Conventions
- **SEO Fields**: Use `SEOMixin` from `core/models/seo.py` for meta titles/descriptions
- **Language Fields**: Individual fields like `name_en`, `description_fr` (not JSON/hstore)
- **User Language Logic**: Check `UserProfile.get_effective_language()` method for preference resolution

### Frontend Structure
- **Dynamic Routes**: `app/[lang]/` for all public pages
- **Admin Panel**: `app/admin/` (language-agnostic)
- **Components**: Use `getUIText(lang)` from `i18n/ui.ts` for translations
- **Middleware**: `middleware.ts` handles locale detection and redirects

### Key Integration Points
- **Language Middleware Chain**: `LocaleMiddleware` → `UserLanguageMiddleware` → `AssistantLanguageMiddleware`
- **API Language Resolution**: URL param → User profile → Session → Cookie → Browser header → Default
- **Arabic Handling**: Special logic for dashboard vs website preferences in middleware

## Essential Files to Understand
- `middleware/language.py` - Complex language preference logic
- `accounts/models.py` - User profile with Arabic preferences  
- `frontend/middleware.ts` - Next.js locale routing
- `frontend/src/i18n/ui.ts` - Frontend translations
- `listacrosseu_project/settings.py` - Django i18n configuration
- `core/models/seo.py` - SEO mixin used across models

## Common Tasks
- **Add new language**: Update `LANGUAGES` in settings + model fields + frontend translations
- **New API endpoint**: Create in app's `urls.py`, use DRF serializers, add CORS if needed
- **Frontend page**: Add to `app/[lang]/` with proper TypeScript typing
- **Database changes**: Always run migrations, check SEO fields inheritance
- **Translation updates**: Use Django's `makemessages`/`compilemessages` workflow

## Development Environment Notes
- Uses SQLite for development (see `docker-compose.yml` for production setup)
- Mock API simulator (`django_api_simulator.js`) available as fallback
- PowerShell scripts (`start_django.ps1`) for Windows development setup