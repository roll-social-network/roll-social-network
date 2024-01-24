"""
timeline models
"""
from django.db import models
from rollsocialnetwork.social.models import UserProfile

class Post(models.Model):
    """
    post model
    """
    user_profile = models.ForeignKey(UserProfile,
                                     on_delete=models.CASCADE,
                                     blank=False)
    photo = models.ImageField(blank=False,
                              upload_to="posts")
    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=False,
                                      editable=False)

    def __str__(self) -> str:
        return f"Post [{self.user_profile}]"
