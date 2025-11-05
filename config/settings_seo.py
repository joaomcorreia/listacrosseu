# Add this to your INSTALLED_APPS in settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Your apps
    'core',  # Contains SEO models and admin
    'listings',  # Your business listings
    'blog',  # Optional blog app
    
    # Third party apps (if any)
    # ...
]

# Optional: Add custom admin site configuration
ADMIN_SITE_HEADER = "ListAcross EU Admin"
ADMIN_SITE_TITLE = "ListAcross EU Admin"
ADMIN_INDEX_TITLE = "Welcome to ListAcross EU Administration"

# SEO-related settings
DEFAULT_SEO_TITLE = "ListAcross EU - European Business Directory"
DEFAULT_SEO_DESCRIPTION = "Find businesses across Europe. Comprehensive directory of European companies, restaurants, hotels, and services."

# Media files (for OG images)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files (for admin CSS/JS)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]