from django.urls import path

from . import consumers

ai_pals_websocket_urlpatterns = [
    path("ws/critter-description/", consumers.CritterGenerationConsumer.as_asgi()),
]
