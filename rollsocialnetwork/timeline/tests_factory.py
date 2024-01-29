"""
timeline tests factory
"""
from rollsocialnetwork.social.tests_factory import UserProfileFactory
from .models import Post


class PostFactory:
    """
    post factory
    """
    def __init__(self) -> None:
        self.user_profile_factory = UserProfileFactory()

    def factory_post(self,
                     user_profile=None):
        """
        factory post
        """
        return {
            "user_profile": user_profile or self.user_profile_factory.create_user_profile(),
        }

    def create_post(self, **kwargs):
        """
        create post
        """
        return Post.objects.create(**self.factory_post(**kwargs))
