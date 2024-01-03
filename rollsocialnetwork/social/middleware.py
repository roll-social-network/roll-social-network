"""
social middlewares
"""
from django.utils.deprecation import MiddlewareMixin
from .models import UserProfile

class CurrentUserProfile(MiddlewareMixin):  # pylint: disable=R0903
    """
    Middleware that sets `user_profile` attribute to request object.
    """
    def process_request(self, request):
        """
        process request
        """
        if request.user.is_authenticated:
            request.user_profile = UserProfile.get_user_profile(request.user, request.site)
