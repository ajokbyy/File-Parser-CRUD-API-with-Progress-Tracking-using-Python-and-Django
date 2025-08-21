import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import files.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'file_parser.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            files.routing.websocket_urlpatterns
        )
    ),
})