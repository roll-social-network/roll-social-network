"""
roll tests factory
"""
from datetime import timedelta
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.utils import timezone
from oauth2_provider.models import (  # type: ignore[import-untyped]
    get_application_model,
    get_access_token_model,
)
from .tests_fake import fake

class SiteFactory:
    """
    site factory
    """
    def factory_site(self, domain=None, name=None):
        """
        factory site
        """
        return {
            "domain": domain or fake.unique.domain_name(),
            "name": name or fake.unique.company(),
        }

    def create_site(self, **kwargs):
        """
        create site
        """
        return Site.objects.create(**self.factory_site(**kwargs))

class UserFactory:
    """
    user factory
    """
    def factory_user(self):
        """
        factory user
        """
        return {"username": fake.unique.e164()}

    def create_user(self):
        """
        create user
        """
        return get_user_model().objects.create(**self.factory_user())

class OAuth2ApplicationFactory:
    """
    oauth2 application factory
    """
    def factory_oauth2_application(self, redirect_uris=None):
        """
        factory oauth2 application
        """
        return {
            "redirect_uris": redirect_uris or None
        }

    def create_oauth2_application(self, **kwargs):
        """
        create oauth2 application
        """
        return get_application_model().objects.create(**self.factory_oauth2_application(**kwargs))

class OAuth2AccessTokenFactory:
    """
    oauth2 access token factory
    """
    def factory_oauth2_access_token(self, user=None, application=None, scope=None, expires=None):
        """
        factory oauth2 access token
        """
        user_factory = UserFactory()
        application_factory = OAuth2ApplicationFactory()
        return {
            "user": user or user_factory.create_user(),
            "application": application or application_factory.create_oauth2_application(),
            "scope": scope or "",
            "expires": expires or (timezone.now() + timedelta(minutes=1))
        }

    def create_oauth2_access_token(self, **kwargs):
        """
        create oauth2 access token
        """
        return get_access_token_model().objects.create(**self.factory_oauth2_access_token(**kwargs))
