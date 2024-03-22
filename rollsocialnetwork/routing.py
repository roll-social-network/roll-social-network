"""
rollsocialnetwork routing
"""

from django.urls import path
from .consumers import WatcherConsumer

websocket_urlpatterns = [
    path("ws/watcher/", WatcherConsumer.as_asgi()),
]
