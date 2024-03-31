"""
roll tests factory
"""
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
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
