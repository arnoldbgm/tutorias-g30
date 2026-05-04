# Django settings for production.
# Inherits from base.py

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')

# Database for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # Example for production DB
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'), # Default to 'db' if using Docker Compose
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

# Static files (CSS, JavaScript, Images) for production
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (User uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# CORS settings for production (if needed)
# CORS_ALLOWED_ORIGINS = [
#     "https://yourdomain.com",
# ]
# CORS_ALLOW_CREDENTIALS = True

# Add any other production-specific settings here
