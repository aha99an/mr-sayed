"""
ASGI config for mr-syed project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.mr-syed.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mr-syed.settings')

application = get_asgi_application()
