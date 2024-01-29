"""
social tests factory
"""
from rollsocialnetwork.tests_factory import (
    SiteFactory,
    UserFactory,
)
from rollsocialnetwork.tests_fake import fake
from .models import UserProfile

class UserProfileFactory:
    """
    user profile factory
    """
    def __init__(self) -> None:
        self.user_factory = UserFactory()
        self.site_factory = SiteFactory()

    def factory_user_profile(self,
                             username=None,
                             user=None,
                             site=None):
        """
        factory user profile
        """
        return {
            "username": username or fake.unique.slug(),
            "user": user or self.user_factory.create_user(),
            "site": site or self.site_factory.create_site(),
        }

    def create_user_profile(self, **kwargs):
        """
        create user profile
        """
        return UserProfile.objects.create(**self.factory_user_profile(**kwargs))
