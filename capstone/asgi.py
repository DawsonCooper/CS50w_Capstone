"""
ASGI config for capstone project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import personnelPlanet.routing
from channels.security.websocket import OriginValidator
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'capstone.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': OriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                personnelPlanet.routing.websocket_urlpatterns
            )
        )
    )
})
