"""
ASGI config for drf_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/

For Channels documentation, see:
https://channels.readthedocs.io/en/latest/installation.html
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from ai_pals.routing import ai_pals_websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drf_project.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(ai_pals_websocket_urlpatterns))
        ),
    }
)
