"""
social models
"""
from typing import Optional
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.urls import reverse
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser

class UserProfile(models.Model):
    """
    user profile
    """
    class Meta:
        unique_together = [
            "username",
            "site",
        ]

    username = models.SlugField()
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             blank=False)
    site = models.ForeignKey(Site,
                             on_delete=models.CASCADE,
                             blank=False)

    @classmethod
    def get_user_profile(cls,
                         user: AbstractBaseUser | AnonymousUser,
                         site: Site) -> Optional['UserProfile']:
        """
        get user profile
        """
        try:
            return cls.objects.get(user=user,
                                   site=site)
        except cls.DoesNotExist:
            return None

    def __str__(self) -> str:
        return f"{self.site}: User Profile @{self.username} ({self.user})"

    def get_absolute_url(self):
        """
        get absolute url
        """
        return reverse("social-user-profile", kwargs={"username": self.username})
