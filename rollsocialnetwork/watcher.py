"""
rollsocialnetwork watcher
"""

from typing import (
    Dict,
    Optional,
    Tuple
)
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer  # type: ignore[import-untyped]

class Watcher:
    """
    Watcher class
    """

    @classmethod
    def build_group_name(cls, model: str, attr: str, pk: Optional[(str | int)]=None) -> str:
        """
        build group name
        """
        return '_'.join([model, str(pk), attr] if pk else [model, attr])

    @classmethod
    def destructe_ref(cls, ref: Dict[str, Optional[str]]) -> Tuple[str, str, Optional[str]]:
        """
        destructe ref
        """
        model = ref.get("model")
        if not model:
            raise ValueError("ref.model field is required")
        attr = ref.get("attr")
        if not attr:
            raise ValueError("ref.attr field is required")
        pk = ref.get("pk")
        return model, attr, pk

    @classmethod
    def notify(cls, model: str, attr: str, value, pk: Optional[(str | int)]=None) -> None:
        """
        notify
        """
        channel_layer = get_channel_layer()
        group_name = cls.build_group_name(model, attr, pk=pk)
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": f"{model}.{attr}",
                "pk": pk,
                "group_name": group_name,
                attr: value
            }
        )
