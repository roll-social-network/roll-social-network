"""
rollsocialnetwork oauth2_validators
"""
from django.conf import settings
from oauth2_provider.oauth2_validators import OAuth2Validator  # type: ignore[import-untyped]
from rollsocialnetwork.http_request import HttpRequest

class RollOAuth2Validator(OAuth2Validator):  # pylint: disable=W0223
    """
    roll OAuth2 Validator
    """
    oidc_claim_scope = {
        "sub": "openid",
        "name": "profile",
        "username": "profile",
        "email": "email",
        "grafana_email": "grafana",
        "grafana_role": "grafana",
        "passwords_email": "passwords",
        "passwords_username": "passwords",
        "group_ids": "groups",
        "group_names": "groups",
        "groups": "groups"
    }

    def get_additional_claims(self, request: HttpRequest):
        claims = {}
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
            grafana_email = f"{username}@monitoring.{settings.SUBDOMAIN_BASE}"
            passwords_email = f"{username}@passwords.{settings.SUBDOMAIN_BASE}"
            groups = user.groups.all()
            claims.update({
                "name": name,
                "username": username,
                "email": email,
                "grafana_email": grafana_email,
                "grafana_role": grafana_role,
                "passwords_email": email or passwords_email,
                "passwords_username": passwords_email,
                "group_ids": [group.id for group in groups],
                "group_names": [group.name for group in groups],
                "groups": { group.id: group.name for group in groups },
            })
        return claims
