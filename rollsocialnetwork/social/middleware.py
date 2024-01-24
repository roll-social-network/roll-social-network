"""
social middlewares
"""
from django.utils.deprecation import MiddlewareMixin
from rollsocialnetwork.http_request import HttpRequest
from .models import UserProfile

class CurrentUserProfile(MiddlewareMixin):  # pylint: disable=R0903
    """
    Middleware that sets `user_profile` attribute to request object.
    """
    def process_request(self, request: HttpRequest):
        """
        process request
        """
        if request.user.is_authenticated:
            request.user_profile = UserProfile.get_user_profile(request.user, request.site)
        else:
            request.user_profile = None
