# Gymnify/wsgi.py
import os
from django.core.wsgi import get_wsgi_application
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gymnify.settings')
application = get_wsgi_application()
