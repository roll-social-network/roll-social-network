"""
oidc backends
"""
from django.conf import settings
from social_core.backends.oauth import BaseOAuth2PKCE  # type: ignore[import-untyped]
from social_core.backends.open_id_connect import OpenIdConnectAuth  # type: ignore[import-untyped]

class RollOpenIdConnectAuth(BaseOAuth2PKCE,  # pylint: disable=W0223
                            OpenIdConnectAuth):
    """
    roll Open ID Connect Auth backend
    """
    name = "roll"
    OIDC_ENDPOINT = settings.OIDC_ENDPOINT
    PKCE_DEFAULT_CODE_CHALLENGE_METHOD = "S256"
    DEFAULT_SCOPE = ["openid"]
    USERNAME_KEY = "username"

    def get_user_details(self, response):
        username_key = self.setting("USERNAME_KEY", self.USERNAME_KEY)
        return {
            "name": response.get("name"),
            "username": response.get(username_key),
            "email": response.get("email"),
        }
