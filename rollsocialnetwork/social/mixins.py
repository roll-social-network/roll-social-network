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
from django.shortcuts import resolve_url
from django.contrib.auth.views import redirect_to_login

class UserProfileRequiredMixin(AccessMixin):
    """
    user profile required mixin
    """
    login_url = settings.CREATE_USER_PROFILE_URL

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            return settings.LOGIN_URL
        if not self.request.user_profile:
            return settings.CREATE_USER_PROFILE_URL
        raise BadRequest("not expected, user authenticated and user profile setted")

    def dispatch(self, request, *args, **kwargs):
        """
        dispatch
        """
        if not request.user.is_authenticated or not request.user_profile:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        if (self.raise_exception or (
            self.request.user.is_authenticated and self.request.user_profile)
        ):
            raise PermissionDenied(self.get_permission_denied_message())
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (not login_scheme or login_scheme == current_scheme) and (
            not login_netloc or login_netloc == current_netloc
        ):
            path = self.request.get_full_path()
        return redirect_to_login(
            path,
            resolved_login_url,
            self.get_redirect_field_name(),
        )
