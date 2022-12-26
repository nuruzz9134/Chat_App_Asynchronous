
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import chat_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_application.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
    'http': application,
    'websocket': AuthMiddlewareStack(
                             URLRouter(
                               chat_app.routing.websocket_urlpatterns
                             ),
                         )
                    })

                    