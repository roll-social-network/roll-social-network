"""
sso apps
"""
from django.apps import AppConfig

class SsoConfig(AppConfig):
    """
    sso config app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rollsocialnetwork.sso'

    def ready(self) -> None:
        import rollsocialnetwork.sso.signals  # pylint: disable=C0415,W0611
