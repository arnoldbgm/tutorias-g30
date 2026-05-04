"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Set default settings module, can be overridden by environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev') # Default to dev settings

application = get_wsgi_application()
