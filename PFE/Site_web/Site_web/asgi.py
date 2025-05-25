import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Site_web.settings")
django.setup()  # ⬅️ AJOUTER CETTE LIGNE AVANT D'IMPORTER models/routing

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import Superviseur.routing  # Ton app qui contient les routes WebSocket

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        Superviseur.routing.websocket_urlpatterns
    ),
})
