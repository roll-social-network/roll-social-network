"""
rollsocialnetwork oauth2_validators
"""
from typing import Dict
from django.conf import settings
from oauth2_provider.oauth2_validators import OAuth2Validator  # type: ignore[import-untyped]
from rollsocialnetwork.http_request import HttpRequest

class RollOAuth2Validator(OAuth2Validator):  # pylint: disable=W0223
    """
    roll OAuth2 Validator
    """
    def get_userinfo_claims(self, request: HttpRequest) -> Dict:
        claims = super().get_userinfo_claims(request)
        user = request.user
        if user.is_authenticated:
            name = user.get_full_name()  # type: ignore[attr-defined]
            username = user.get_username()
            email = user.email  # type: ignore[attr-defined]
            grafana_role = "Viewer"
            if user.is_staff:  # type: ignore[attr-defined]
                grafana_role = "Editor"
            if user.is_superuser:  # type: ignore[attr-defined]
                grafana_role = "Admin"
            claims.update({
                "name": name,
                "username": username,
                "email": email,
                "grafana": {
                    "email": email or f"{username}@monitoring.{settings.SUBDOMAIN_BASE}",
                    "role": grafana_role
                }
            })
        return claims
