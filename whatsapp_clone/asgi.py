"""
ASGI config for whatsapp_clone project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Set the settings module environment variable.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whatsapp_clone.settings')

# Initialize the Django ASGI application early to ensure settings are configured.
django_asgi_app = get_asgi_application()

# Now, import the Channels components.
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests.
    "http": django_asgi_app,

    # WebSocket chat handler.
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
