# ListAcross EU - Complete Project Setup Guide

A comprehensive step-by-step guide to build the ListAcross EU bilingual business directory platform from scratch.

## Project Overview

ListAcross EU is a **bilingual Django + Next.js** business directory platform targeting European markets with:
- **Backend**: Django 4.2+ with Django REST Framework
- **Frontend**: Next.js 14 with TypeScript and Tailwind CSS  
- **Languages**: EN, FR, NL, PT, DE, ES, AR (with RTL support)
- **Architecture**: API-first with proxy integration
- **Database**: SQLite (development), PostgreSQL (production)

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Django Backend Setup](#django-backend-setup)
4. [Next.js Frontend Setup](#nextjs-frontend-setup)
5. [Database Configuration](#database-configuration)
6. [Multi-language Setup](#multi-language-setup)
7. [API Integration](#api-integration)
8. [Authentication System](#authentication-system)
9. [Admin Panel Configuration](#admin-panel-configuration)
10. [AI Integration Setup](#ai-integration-setup)
11. [Development Workflow](#development-workflow)
12. [Production Deployment](#production-deployment)
13. [Troubleshooting](#troubleshooting)

---

## 1. Prerequisites

### System Requirements

- **Operating System**: Windows 10/11, macOS, or Linux
- **Python**: 3.9+ (Recommended: 3.12)
- **Node.js**: 18+ (LTS version recommended)
- **Git**: Latest version
- **Code Editor**: VS Code (recommended) with Python and TypeScript extensions

### Windows-Specific Requirements

```cmd
# Ensure you're using Command Prompt (CMD), not PowerShell
# Verify versions
python --version
node --version
npm --version
git --version
```

### Install Required Tools

1. **Python**: Download from [python.org](https://python.org)
2. **Node.js**: Download from [nodejs.org](https://nodejs.org)
3. **Git**: Download from [git-scm.com](https://git-scm.com)

---

## 2. Environment Setup

### Create Project Directory

```cmd
# Create main project directory
mkdir C:\projects
cd /d C:\projects

# Clone or create project
git clone https://github.com/joaomcorreia/listacrosseu.git
cd listacrosseu
```

### Python Virtual Environment (Recommended)

```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Environment Variables

Create `.env` file in project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database
DATABASE_URL=sqlite:///db.sqlite3

# AI Integration
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key

# CORS Settings
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Media Settings
MEDIA_URL=/media/
MEDIA_ROOT=media/
```

---

## 3. Django Backend Setup

### Install Django Dependencies

```cmd
# Navigate to project root
cd /d C:\projects\listacrosseu

# Install Python dependencies
pip install -r requirements.txt
```

### Core Requirements (requirements.txt)

```txt
Django>=5.1.0,<5.2.0
djangorestframework>=3.14.0
django-cors-headers>=4.0.0
django-filter>=23.2
Pillow>=10.0.0
python-decouple>=3.8

# AI Dependencies
openai>=1.40.0
anthropic>=0.39.0
requests>=2.32.3
```

### Django Project Structure

```
listacrosseu/
├── manage.py
├── listacrosseu_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/          # User management
├── listings/          # Business listings
├── blog/             # Blog system with AI
├── core/             # Core utilities
├── middleware/       # Custom middleware
├── seo/              # SEO optimization
├── sliders/          # Homepage sliders
└── templates/        # Django templates
```

### Settings Configuration (settings.py)

```python
import os
from decouple import config

# Basic Django Settings
SECRET_KEY = config('SECRET_KEY', default='your-secret-key')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')

# Internationalization
LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
    ('fr', 'Français'),
    ('nl', 'Nederlands'),
    ('pt', 'Português'),
    ('de', 'Deutsch'),
    ('es', 'Español'),
    ('ar', 'العربية'),
]

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'corsheaders',
    'django_filters',
    
    # Local apps
    'accounts',
    'listings',
    'blog',
    'core',
    'seo',
    'sliders',
]

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'middleware.language.UserLanguageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}

# CORS Settings
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=True, cast=bool)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### Create Django Apps

```cmd
# Create core apps
python manage.py startapp accounts
python manage.py startapp listings  
python manage.py startapp blog
python manage.py startapp core
python manage.py startapp seo
python manage.py startapp sliders
```

### Database Migration

```cmd
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

---

## 4. Next.js Frontend Setup

### Create Frontend Directory

```cmd
# Navigate to project root
cd /d C:\projects\listacrosseu

# Create Next.js application
npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"

# Navigate to frontend
cd frontend
```

### Frontend Dependencies (package.json)

```json
{
  "name": "listacrosseu-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "dev:3000": "next dev --port 3000",
    "dev:3001": "next dev --port 3001",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "clean": "rimraf .next .turbo node_modules/.cache"
  },
  "dependencies": {
    "@heroicons/react": "^2.2.0",
    "@tailwindcss/forms": "^0.5.10",
    "@tailwindcss/line-clamp": "^0.4.4",
    "next": "^14.2.33",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "react-hot-toast": "^2.6.0",
    "uuid": "^13.0.0"
  },
  "devDependencies": {
    "@types/node": "20.10.6",
    "@types/react": "18.2.46",
    "@types/react-dom": "18.2.18",
    "@types/uuid": "^10.0.0",
    "autoprefixer": "^10.4.16",
    "eslint": "8.56.0",
    "eslint-config-next": "14.0.4",
    "postcss": "^8.4.32",
    "rimraf": "^6.1.0",
    "tailwindcss": "^3.4.0",
    "typescript": "5.3.3"
  }
}
```

### Install Frontend Dependencies

```cmd
# Navigate to frontend directory
cd /d C:\projects\listacrosseu\frontend

# Install dependencies
npm install
```

### Next.js Configuration (next.config.js)

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  
  // API Proxy to Django
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://127.0.0.1:8000/api/:path*',
      },
    ]
  },
  
  // Image optimization
  images: {
    domains: ['localhost', '127.0.0.1'],
    remotePatterns: [
      {
        protocol: 'http',
        hostname: '127.0.0.1',
        port: '8000',
        pathname: '/media/**',
      },
    ],
  },
  
  // Internationalization
  i18n: {
    locales: ['en', 'fr', 'nl', 'pt', 'de', 'es', 'ar'],
    defaultLocale: 'en',
    localeDetection: false,
  },
}

module.exports = nextConfig
```

### Frontend Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── [lang]/           # Dynamic language routing
│   │   │   ├── page.tsx      # Homepage
│   │   │   ├── businesses/   # Business listings
│   │   │   ├── blog/         # Blog pages
│   │   │   └── layout.tsx    # Language layout
│   │   ├── admin/            # Admin pages
│   │   │   ├── blog/         # Blog management
│   │   │   ├── businesses/   # Business management
│   │   │   └── layout.tsx    # Admin layout
│   │   ├── globals.css       # Global styles
│   │   └── layout.tsx        # Root layout
│   ├── components/           # Reusable components
│   │   ├── ScrollNavbar.tsx  # Dynamic navigation
│   │   ├── LanguageSwitcher.tsx
│   │   └── ui/               # UI components
│   ├── i18n/
│   │   ├── ui.ts            # Frontend translations
│   │   └── types.ts         # Language types
│   └── types/               # TypeScript definitions
├── middleware.ts            # Next.js middleware
├── tailwind.config.js       # Tailwind configuration
└── package.json
```

---

## 5. Database Configuration

### Model Design

**Core Models Structure:**

```python
# accounts/models.py
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_language = models.CharField(max_length=5, default='en')
    arabic_on_dashboard = models.BooleanField(default=False)
    arabic_on_website = models.BooleanField(default=False)
    
    def get_effective_language(self):
        """Complex language resolution logic"""
        # Implementation for Arabic preferences
        pass

# listings/models.py  
class Business(models.Model):
    # Multi-language fields
    name_en = models.CharField(max_length=200)
    name_fr = models.CharField(max_length=200, blank=True)
    name_nl = models.CharField(max_length=200, blank=True)
    # ... other language fields
    
    description_en = models.TextField()
    description_fr = models.TextField(blank=True)
    # ... other language fields
    
    slug = models.SlugField(unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

# blog/models.py
class BlogPost(models.Model):
    title_en = models.CharField(max_length=200)
    title_fr = models.CharField(max_length=200, blank=True)
    # ... other language fields
    
    content_en = models.TextField()
    content_fr = models.TextField(blank=True)
    # ... other language fields
    
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

### SEO Mixin

```python
# core/models/seo.py
class SEOMixin(models.Model):
    meta_title_en = models.CharField(max_length=60, blank=True)
    meta_title_fr = models.CharField(max_length=60, blank=True)
    # ... other language fields
    
    meta_description_en = models.TextField(max_length=160, blank=True)
    meta_description_fr = models.TextField(max_length=160, blank=True)
    # ... other language fields
    
    class Meta:
        abstract = True
```

### Migration Commands

```cmd
# Generate migrations for all apps
python manage.py makemigrations accounts
python manage.py makemigrations listings
python manage.py makemigrations blog
python manage.py makemigrations core
python manage.py makemigrations seo
python manage.py makemigrations sliders

# Apply all migrations
python manage.py migrate
```

---

## 6. Multi-language Setup

### Custom Language Middleware

```python
# middleware/language.py
from django.utils import translation
from django.conf import settings

class UserLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Language resolution priority:
        # 1. URL parameter (?lang=xx)
        # 2. User profile preference
        # 3. Session language
        # 4. Cookie language
        # 5. Browser Accept-Language
        # 6. Default language
        
        language = self.get_language_for_request(request)
        translation.activate(language)
        request.LANGUAGE_CODE = language
        
        response = self.get_response(request)
        return response
        
    def get_language_for_request(self, request):
        # Complex language resolution logic
        # Handle Arabic dashboard/website preferences
        pass
```

### Translation Files Setup

```cmd
# Create translation directories
mkdir locale
mkdir locale\en\LC_MESSAGES
mkdir locale\fr\LC_MESSAGES
mkdir locale\nl\LC_MESSAGES
mkdir locale\pt\LC_MESSAGES
mkdir locale\de\LC_MESSAGES
mkdir locale\es\LC_MESSAGES
mkdir locale\ar\LC_MESSAGES

# Generate translation files
python manage.py makemessages -l fr
python manage.py makemessages -l nl  
python manage.py makemessages -l pt
python manage.py makemessages -l de
python manage.py makemessages -l es
python manage.py makemessages -l ar

# Compile translations
python manage.py compilemessages
```

### Frontend Translations

```typescript
// src/i18n/ui.ts
export const ui = {
  en: {
    'nav.home': 'Home',
    'nav.businesses': 'Businesses',
    'nav.blog': 'Blog',
    'nav.admin': 'Admin',
  },
  fr: {
    'nav.home': 'Accueil',
    'nav.businesses': 'Entreprises', 
    'nav.blog': 'Blog',
    'nav.admin': 'Admin',
  },
  // ... other languages
} as const

export function getUIText(lang: string) {
  return ui[lang as keyof typeof ui] || ui.en
}
```

### Dynamic Language Routing

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname
  const pathnameIsMissingLocale = [
    'en', 'fr', 'nl', 'pt', 'de', 'es', 'ar'
  ].every(
    (locale) => !pathname.startsWith(`/${locale}/`) && pathname !== `/${locale}`
  )

  if (pathnameIsMissingLocale) {
    return NextResponse.redirect(
      new URL(`/en${pathname}`, request.url)
    )
  }
}
```

---

## 7. API Integration

### Django REST Framework Setup

```python
# listings/serializers.py
from rest_framework import serializers
from .models import Business, Category

class BusinessSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    
    class Meta:
        model = Business
        fields = ['id', 'name', 'description', 'slug', 'category']
    
    def get_name(self, obj):
        lang = self.context.get('language', 'en')
        return getattr(obj, f'name_{lang}', obj.name_en)
    
    def get_description(self, obj):
        lang = self.context.get('language', 'en')
        return getattr(obj, f'description_{lang}', obj.description_en)

# listings/views.py
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['language'] = self.request.GET.get('lang', 'en')
        return context
```

### API URLs Configuration

```python
# listacrosseu_project/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from listings.views import BusinessViewSet

router = DefaultRouter()
router.register(r'businesses', BusinessViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/auth/', include('accounts.urls')),
    path('api/v1/blog/', include('blog.urls')),
]
```

### Frontend API Integration

```typescript
// src/types/api.ts
export interface Business {
  id: number
  name: string
  description: string
  slug: string
  category: number
}

// src/lib/api.ts
const API_BASE = '/api/v1'

export async function getBusinesses(lang: string = 'en'): Promise<Business[]> {
  const response = await fetch(`${API_BASE}/businesses/?lang=${lang}`)
  if (!response.ok) throw new Error('Failed to fetch businesses')
  return response.json()
}

export async function getBusiness(slug: string, lang: string = 'en'): Promise<Business> {
  const response = await fetch(`${API_BASE}/businesses/${slug}/?lang=${lang}`)
  if (!response.ok) throw new Error('Failed to fetch business')
  return response.json()
}
```

---

## 8. Authentication System

### Django Authentication

```python
# accounts/models.py
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_language = models.CharField(
        max_length=5, 
        choices=[('en', 'English'), ('fr', 'French'), ('nl', 'Dutch'), 
                ('pt', 'Portuguese'), ('de', 'German'), ('es', 'Spanish'), 
                ('ar', 'Arabic')],
        default='en'
    )
    arabic_on_dashboard = models.BooleanField(default=False)
    arabic_on_website = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# accounts/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate, login

class AuthViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({'success': True})
        return Response({'error': 'Invalid credentials'}, 
                       status=status.HTTP_401_UNAUTHORIZED)
```

### Frontend Authentication

```typescript
// src/lib/auth.ts
export interface User {
  id: number
  username: string
  email: string
  profile: {
    preferred_language: string
    arabic_on_dashboard: boolean
    arabic_on_website: boolean
  }
}

export async function login(username: string, password: string): Promise<User> {
  const response = await fetch('/api/auth/login/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password }),
  })
  
  if (!response.ok) throw new Error('Login failed')
  return response.json()
}

export async function getCurrentUser(): Promise<User | null> {
  try {
    const response = await fetch('/api/auth/user/')
    if (!response.ok) return null
    return response.json()
  } catch {
    return null
  }
}
```

---

## 9. Admin Panel Configuration

### Django Admin Enhancement

```python
# listings/admin.py
from django.contrib import admin
from .models import Business, Category

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name_en', 'name_fr', 'name_nl']
    prepopulated_fields = {'slug': ('name_en',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('slug', 'category')
        }),
        ('English', {
            'fields': ('name_en', 'description_en')
        }),
        ('French', {
            'fields': ('name_fr', 'description_fr'),
            'classes': ('collapse',)
        }),
        # ... other language fieldsets
    )

# blog/admin.py
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'author', 'published', 'created_at']
    list_filter = ['published', 'created_at', 'author']
    search_fields = ['title_en', 'title_fr', 'content_en']
    prepopulated_fields = {'slug': ('title_en',)}
```

### Next.js Admin Interface

```typescript
// src/app/admin/layout.tsx
export default function AdminLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex justify-between h-16">
            <div className="flex">
              <Link href="/admin" className="flex items-center px-4">
                Admin Panel
              </Link>
              <div className="flex space-x-8">
                <Link href="/admin/businesses">Businesses</Link>
                <Link href="/admin/blog">Blog</Link>
                <Link href="/admin/users">Users</Link>
              </div>
            </div>
          </div>
        </div>
      </nav>
      <main>{children}</main>
    </div>
  )
}

// src/app/admin/blog/posts/new/page.tsx - AI-Enhanced Blog Creation
export default function NewBlogPost() {
  const [topic, setTopic] = useState('')
  const [titleSuggestions, setTitleSuggestions] = useState<string[]>([])
  const [selectedTitle, setSelectedTitle] = useState('')
  
  const generateTitleSuggestions = async () => {
    try {
      const response = await fetch('/api/v1/ai/generate/titles/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic }),
      })
      const data = await response.json()
      setTitleSuggestions(data.suggestions)
    } catch (error) {
      // Fallback to mock suggestions
      setTitleSuggestions([
        `The Ultimate Guide to ${topic}`,
        `${topic}: Best Practices and Tips`,
        `Everything You Need to Know About ${topic}`,
      ])
    }
  }
  
  // Implementation continues...
}
```

---

## 10. AI Integration Setup

### OpenAI & Anthropic Configuration

```python
# blog_ai/providers.py
import openai
import anthropic
from django.conf import settings

class AIProvider:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.anthropic_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    def generate_blog_titles(self, topic: str, language: str = 'en') -> list:
        prompt = f"""Generate 5 engaging blog post titles about "{topic}" 
                    in {language}. Make them SEO-friendly and compelling."""
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200
            )
            return response.choices[0].message.content.strip().split('\n')
        except Exception:
            # Fallback to Anthropic
            return self._anthropic_fallback(prompt)
    
    def _anthropic_fallback(self, prompt: str) -> list:
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip().split('\n')
        except Exception:
            # Final fallback
            return ["AI service unavailable - using fallback titles"]

# blog/views.py - AI API Endpoints
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .ai_providers import AIProvider

@api_view(['POST'])
def generate_title_suggestions(request):
    topic = request.data.get('topic', '')
    language = request.data.get('language', 'en')
    
    if not topic:
        return Response({'error': 'Topic is required'}, status=400)
    
    ai_provider = AIProvider()
    suggestions = ai_provider.generate_blog_titles(topic, language)
    
    return Response({
        'suggestions': suggestions,
        'topic': topic,
        'language': language
    })
```

### Frontend AI Integration

```typescript
// src/lib/ai.ts
export interface TitleSuggestion {
  suggestions: string[]
  topic: string
  language: string
}

export async function generateTitleSuggestions(
  topic: string, 
  language: string = 'en'
): Promise<TitleSuggestion> {
  const response = await fetch('/api/v1/ai/generate/titles/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrfToken(),
    },
    body: JSON.stringify({ topic, language }),
  })
  
  if (!response.ok) {
    throw new Error('Failed to generate suggestions')
  }
  
  return response.json()
}

function getCsrfToken(): string {
  return document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
}
```

---

## 11. Development Workflow

### Startup Scripts

**Windows CMD Scripts:**

```cmd
REM start-django-backend.cmd
@echo off
cd /d C:\projects\listacrosseu
echo Starting Django backend on port 8000...
python manage.py runserver 127.0.0.1:8000
```

```cmd
REM start-nextjs-frontend.cmd  
@echo off
cd /d C:\projects\listacrosseu\frontend
echo Starting Next.js frontend on port 3000...
npm run dev:3000
```

```cmd
REM start-dev-environment.cmd
@echo off
echo Starting ListAcross EU Development Environment...
start "Django Backend" cmd /k "C:\projects\listacrosseu\start-django-backend.cmd"
timeout /t 3
start "Next.js Frontend" cmd /k "C:\projects\listacrosseu\start-nextjs-frontend.cmd"
echo Development servers started!
echo Django: http://127.0.0.1:8000
echo Next.js: http://localhost:3000
```

### VS Code Tasks Configuration

```json
// .vscode/tasks.json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Start Django Backend",
            "type": "shell",
            "command": "cd /d c:\\projects\\listacrosseu && python manage.py runserver 127.0.0.1:8000",
            "group": "build",
            "isBackground": true,
            "options": {
                "shell": {
                    "executable": "cmd.exe",
                    "args": ["/c"]
                }
            }
        },
        {
            "label": "Start Next.js Frontend",
            "type": "shell", 
            "command": "c:\\projects\\listacrosseu\\frontend\\start-frontend.cmd",
            "group": {"kind": "build", "isDefault": true},
            "isBackground": false,
            "options": {
                "shell": {
                    "executable": "cmd.exe",
                    "args": ["/c"]
                }
            }
        },
        {
            "label": "Clean Next.js Cache",
            "type": "shell",
            "command": "cd /d c:\\projects\\listacrosseu\\frontend && npm run clean",
            "group": "build"
        }
    ]
}
```

### Development Checklist

**Daily Development Workflow:**

1. **Start Development Servers**
   ```cmd
   # Terminal 1: Django Backend
   cd /d C:\projects\listacrosseu
   python manage.py runserver 127.0.0.1:8000
   
   # Terminal 2: Next.js Frontend
   cd /d C:\projects\listacrosseu\frontend
   npm run dev:3000
   ```

2. **Make Changes**
   - Backend: Edit Django models, views, serializers
   - Frontend: Edit React components, pages, styles
   - Translations: Update message files as needed

3. **Test Changes**
   - Backend API: `http://127.0.0.1:8000/api/v1/`
   - Frontend: `http://localhost:3000`
   - Admin: `http://127.0.0.1:8000/admin/`

4. **Database Updates**
   ```cmd
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Translation Updates**
   ```cmd
   python manage.py makemessages -l fr -l nl -l pt -l de -l es -l ar
   python manage.py compilemessages
   ```

---

## 12. Production Deployment

### Environment Configuration

**Production Settings (settings_production.py):**

```python
from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

# Static files
STATIC_ROOT = '/var/www/static/'
MEDIA_ROOT = '/var/www/media/'

# Security
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Docker Configuration

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.production.txt .
RUN pip install -r requirements.production.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "listacrosseu_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```yaml
# docker-compose.production.yml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: listacrosseu
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data/

  web:
    build: .
    command: gunicorn listacrosseu_project.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - static_volume:/app/static
      - media_volume:/app/media
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://postgres:${DB_PASSWORD}@db:5432/listacrosseu

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### Deployment Commands

```cmd
# Build and deploy
docker-compose -f docker-compose.production.yml build
docker-compose -f docker-compose.production.yml up -d

# Run migrations
docker-compose -f docker-compose.production.yml exec web python manage.py migrate

# Create superuser
docker-compose -f docker-compose.production.yml exec web python manage.py createsuperuser

# Collect static files
docker-compose -f docker-compose.production.yml exec web python manage.py collectstatic --noinput
```

---

## 13. Troubleshooting

### Common Issues and Solutions

#### 1. "Module not found" errors
```cmd
# Solution: Install missing dependencies
pip install django-filter
pip install -r requirements.txt
```

#### 2. Port already in use
```cmd
# Check what's using the port
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Kill process by PID
taskkill /PID <pid> /F
```

#### 3. Next.js build errors
```cmd
# Clean cache and rebuild
cd /d C:\projects\listacrosseu\frontend
npm run clean
rm -rf node_modules package-lock.json
npm install
npm run build
```

#### 4. Database migration issues
```cmd
# Reset migrations (development only)
python manage.py migrate accounts zero
python manage.py migrate listings zero
python manage.py makemigrations
python manage.py migrate
```

#### 5. CORS errors
- Ensure `django-cors-headers` is installed
- Verify CORS settings in Django settings
- Check Next.js proxy configuration

#### 6. Translation not working
```cmd
# Regenerate translation files
python manage.py makemessages -a
python manage.py compilemessages

# Check middleware order in settings.py
```

### Performance Optimization

1. **Database Optimization**
   - Add database indexes for frequently queried fields
   - Use `select_related` and `prefetch_related` in Django queries
   - Implement database connection pooling

2. **Frontend Optimization**
   - Enable Next.js image optimization
   - Implement lazy loading for components
   - Use React.memo for expensive components
   - Optimize bundle size with dynamic imports

3. **Caching Strategy**
   - Implement Redis for session storage
   - Cache API responses in frontend
   - Use Django's caching framework for database queries

### Monitoring and Logging

```python
# settings.py - Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

---

## Final Setup Verification

### Testing Checklist

✅ **Backend Tests**
- [ ] Django server starts without errors
- [ ] Admin panel accessible at `/admin/`
- [ ] API endpoints return expected data
- [ ] User authentication works
- [ ] Multi-language content displays correctly

✅ **Frontend Tests**
- [ ] Next.js development server starts
- [ ] Pages load without JavaScript errors  
- [ ] Language switching works
- [ ] API integration functions properly
- [ ] Admin panel UI is functional

✅ **Integration Tests**
- [ ] CORS configuration allows frontend requests
- [ ] Authentication state persists across requests
- [ ] File uploads work correctly
- [ ] AI features generate appropriate responses
- [ ] Multi-language content synchronizes

✅ **Production Readiness**
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Static files collected
- [ ] Security settings enabled
- [ ] Performance monitoring configured

---

## Conclusion

This comprehensive setup guide provides everything needed to build the ListAcross EU project from scratch. The architecture supports:

- **Scalable multi-language content management**
- **Modern React/Next.js frontend with TypeScript**
- **Robust Django REST API backend**
- **AI-enhanced content creation**
- **Production-ready deployment configuration**

For ongoing development, refer to the individual documentation files and maintain the established patterns for consistency and maintainability.

---

**Next Steps:**
1. Follow the setup steps in order
2. Test each component as you build it
3. Customize the content and styling to match your requirements
4. Deploy to your production environment
5. Monitor and optimize performance as needed

**Support Resources:**
- Django Documentation: https://docs.djangoproject.com/
- Next.js Documentation: https://nextjs.org/docs
- Django REST Framework: https://www.django-rest-framework.org/
- Project Repository: https://github.com/joaomcorreia/listacrosseu