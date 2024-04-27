"""
sso signals
"""
import logging
from django.conf import settings
from django.db.models import signals
from django.dispatch import receiver  # type: ignore[attr-defined]
from django.contrib.sites.models import Site
from oauth2_provider.models import Application  # type: ignore[import-untyped]

logger = logging.getLogger(__name__)

@receiver([signals.post_save], sender=Site)
def append_redirect_uris_sso_oauth2_application(instance: Site, **kwargs):
    """
    append redirect uris sso oauth2 application
    """
    if settings.ROLL_OAUTH2_APPLICATION_ID:
        try:
            application = Application.objects.get(id=settings.ROLL_OAUTH2_APPLICATION_ID)
            new_uri = settings.ROLL_APPLICATION_REDIRECT_URI_TEMPLATE.format(domain=instance.domain)
            application.redirect_uris += f"\n{new_uri}"
            application.save(update_fields=["redirect_uris"])
        except Application.DoesNotExist:
            logger.warning("Application with ID %s not found",
                           settings.ROLL_OAUTH2_APPLICATION_ID)
