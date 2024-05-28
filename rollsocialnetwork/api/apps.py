"""
api apps
"""
from django.apps import AppConfig

class APIConfig(AppConfig):
    """
    api app config
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "rollsocialnetwork.api"
