"""
WSGI config for certificate project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this files, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ikramqa.settings_prod')

application = get_wsgi_application()
