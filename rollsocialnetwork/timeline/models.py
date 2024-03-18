"""
timeline models
"""
from typing import (
    Optional,
    Type,
)
from django.db import models
from django.contrib.auth.models import AbstractUser
from rollsocialnetwork.social.models import UserProfile

class Post(models.Model):
    """
    post model
    """
    class Meta:
        ordering = ['-created_at']

    user_profile = models.ForeignKey(UserProfile,
                                     on_delete=models.CASCADE,
                                     blank=False,
                                     related_name='posts')
    photo = models.ImageField(max_length=256,
                              blank=False,
                              upload_to="posts")
    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=False,
                                      editable=False)

    def __str__(self) -> str:
        return f"Post [{self.user_profile}]"

    def get_like(self, user_profile: UserProfile) -> Optional["Like"]:
        """
        get like
        """
        try:
            return Like.objects.get(user_profile=user_profile,
                                    post=self)
        except Like.DoesNotExist:
            return None

    def _like(self, user_profile: UserProfile):
        return Like.objects.create(user_profile=user_profile,
                                   post=self)

    def _dislike(self, like: "Like"):
        return like.delete()

    def like_dislike(self, user_profile: UserProfile) -> Optional["Like"]:
        """
        like dislike
        """
        like = self.get_like(user_profile)
        if not like:
            return self._like(user_profile)
        self._dislike(like)
        return None

    def has_user_like(self, user: Type[AbstractUser]) -> bool:
        """
        has user like
        """
        return Like.objects.filter(user_profile__user=user,
                                   post=self).count() > 0

class Like(models.Model):
    """
    like model
    """
    class Meta:
        unique_together = [
            "user_profile",
            "post",
        ]

    user_profile = models.ForeignKey(UserProfile,
                                     on_delete=models.CASCADE,
                                     blank=False)
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             blank=True)
    liked_at = models.DateTimeField(auto_now_add=True,
                                    blank=False,
                                    editable=False)

    def __str__(self) -> str:
        return f"Like {self.user_profile} at {self.post}"
