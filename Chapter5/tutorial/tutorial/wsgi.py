"""
WSGI config for tutorial project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from tutorial.settings import configure_structlog

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutorial.settings')
configure_structlog()
application = get_wsgi_application()





