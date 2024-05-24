"""
oidc pipelines
"""
from typing import (
    Any,
    Optional,
    Dict,
    List,
)
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from social_core.backends.base import BaseAuth  # type: ignore[import-untyped]
from social_core.exceptions import AuthException  # type: ignore[import-untyped]
from .backends import RollOpenIdConnectAuth

def associate_roll_user(backend: BaseAuth,
                        details: Dict,
                        *args: List[Any],
                        user: Optional[AbstractBaseUser] = None,
                        **kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    associate roll user pipe
    """
    if user or not isinstance(backend, RollOpenIdConnectAuth):
        return None
    username = details.get("username")
    if not username:
        return None
    user_class = get_user_model()
    try:
        return {
            "user": user_class.objects.get(username=username),
            "is_new": False
        }
    except user_class.DoesNotExist as e:
        raise AuthException(backend, "roll user not found") from e
