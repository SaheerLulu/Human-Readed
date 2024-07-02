from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/streamapp/', consumers.StreamConsumer.as_asgi()),
]
