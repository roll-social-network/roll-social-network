"""
rollsocialnetwork consumers
"""
from typing import Dict
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer  # type: ignore[import-untyped]
from .watcher import Watcher

class WatcherConsumer(JsonWebsocketConsumer):
    """
    watcher consumer
    """

    def connect(self):
        self.accept()

    def receive_json(self, content: Dict, **kwargs) -> None:
        """
        receive json
        """
        ref = content.get("ref")
        if not ref:
            raise ValueError("ref field not found")
        model, attr, pk = Watcher.destructe_ref(ref)
        group_name = Watcher.build_group_name(model, attr, pk=pk)
        async_to_sync(self.channel_layer.group_add)(
            group_name,
            self.channel_name
        )

    def posts_likes_count(self, data: Dict) -> None:
        """
        type: posts.likes_count
        """
        self.send_json(data)
