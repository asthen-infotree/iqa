"""
ASGI config for certificate project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this files, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ikramqa.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ikramqa.settings_prod')
application = get_asgi_application()
