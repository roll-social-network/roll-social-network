"""
oidc apps
"""
from django.apps import AppConfig

class OIDCConfig(AppConfig):
    """
    oidc config app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rollsocialnetwork.oidc'

    def ready(self) -> None:
        import rollsocialnetwork.oidc.signals  # pylint: disable=C0415,W0611
