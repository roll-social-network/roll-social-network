"""
social mixins
"""
from urllib.parse import urlparse
from django.conf import settings
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import (
    PermissionDenied,
    BadRequest,
)
from django.http import JsonResponse
from django.shortcuts import resolve_url
from django.contrib.auth.views import redirect_to_login
from django.utils.translation import gettext_lazy as _

class UserProfileRequiredMixin(AccessMixin):
    """
    user profile required mixin
    """
    login_url = settings.CREATE_USER_PROFILE_URL

    @property
    def is_action_component(self):
        """
        is action component?
        """
        return "Action-Component" in self.request.headers.keys()

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            return settings.LOGIN_URL
        if not hasattr(self.request, "user_profile") or not self.request.user_profile:
            return settings.CREATE_USER_PROFILE_URL
        raise BadRequest("not expected, user authenticated and user profile setted")

    def get_permission_denied_message(self):
        if not self.request.user.is_authenticated:
            return _("You are not authenticated.")
        if not hasattr(self.request, "user_profile") or not self.request.user_profile:
            return _("You do not have a user profile on this roll.")
        raise BadRequest("not expected, user authenticated and user profile setted")

    def get_action_message(self):
        """
        get action message
        """
        if not self.request.user.is_authenticated:
            return _("Authenticate")
        if not hasattr(self.request, "user_profile") or not self.request.user_profile:
            return _("Create a profile")
        raise BadRequest("not expected, user authenticated and user profile setted")

    def get_action_url(self):
        """
        get action url
        """
        resolved_url = resolve_url(self.get_login_url())
        if not self.is_action_component:
            return resolved_url
        scheme, netloc = urlparse(resolved_url)[:2]
        if scheme and netloc:
            return resolved_url
        path = self.request.build_absolute_uri()
        current_scheme, current_netloc = urlparse(path)[:2]
        scheme = settings.OVERRIDE_SCHEME or current_scheme
        return f"{scheme}://{current_netloc}{resolved_url}"

    def dispatch(self, request, *args, **kwargs):
        """
        dispatch
        """
        if not request.user.is_authenticated \
            or not hasattr(request, "user_profile") \
                or not request.user_profile:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        action_url = self.get_action_url()
        path = self.request.build_absolute_uri()
        action_scheme, action_netloc = urlparse(action_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (not action_scheme or action_scheme == current_scheme) and (
            not action_netloc or action_netloc == current_netloc
        ):
            path = self.request.get_full_path()
        if self.is_action_component:
            return JsonResponse({
                "message": self.get_permission_denied_message(),
                "action_message": self.get_action_message(),
                "action_url": action_url,
                "action_component": "popup-opener-callback",
                "next": path,
            }, status=403)
        return redirect_to_login(
            path,
            action_url,
            self.get_redirect_field_name(),
        )
