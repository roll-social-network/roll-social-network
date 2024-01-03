"""
social decorators
"""
from functools import wraps
from urllib.parse import urlparse

from django.contrib.auth.decorators import REDIRECT_FIELD_NAME
from django.shortcuts import resolve_url
from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from .models import UserProfile

def has_user_profile_test(test_func,
                          redirect_field_name=REDIRECT_FIELD_NAME,
                          create_user_profile_url=settings.CREATE_USER_PROFILE_URL):
    """
    has user profile test decorator builder
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapper_view(request, *args, **kwargs):
            if test_func(request.user, request.site):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(create_user_profile_url)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if (not login_scheme or login_scheme == current_scheme) and (
                not login_netloc or login_netloc == current_netloc):
                path = request.get_full_path()
            return redirect_to_login(path, resolved_login_url, redirect_field_name)
        return _wrapper_view
    return decorator

def user_profile_required(function=None,
                          redirect_field_name=REDIRECT_FIELD_NAME,
                          create_user_profile_url=settings.CREATE_USER_PROFILE_URL):
    """
    user profile required decorator
    """
    actual_decorator = has_user_profile_test(UserProfile.get_user_profile,
                                             redirect_field_name=redirect_field_name,
                                             create_user_profile_url=create_user_profile_url)
    if function:
        return actual_decorator(function)
    return actual_decorator
