# Django settings for development.
# Inherits from base.py

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Add any specific development settings here
# Example: Email backend for testing
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CORS settings for development (if needed)
# Uncomment and configure if you're using a separate frontend on a different origin
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000", # Example for a React frontend
#     "http://127.0.0.1:3000",
# ]
# CORS_ALLOW_CREDENTIALS = True

