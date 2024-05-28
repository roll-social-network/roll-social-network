"""
oauth2 urls
"""
from django.urls import path
from django.conf import settings
from oauth2_provider.urls import (  # type: ignore[import-untyped]
    app_name,
    management_urlpatterns,
    oidc_urlpatterns,
)
from oauth2_provider import views as oauth2_provider_views  # type: ignore[import-untyped]
from .views import RedirectToSSOAppAuthorizeURL

base_urlpatterns = [
    path("authorize/",
         RedirectToSSOAppAuthorizeURL.as_view() \
            if settings.SSO_APP_AUTHORIZE_URL else \
                oauth2_provider_views.AuthorizationView.as_view(),
         name="authorize"),
    path("token/",
         oauth2_provider_views.TokenView.as_view(),
         name="token"),
    path("revoke_token/",
         oauth2_provider_views.RevokeTokenView.as_view(),
         name="revoke-token"),
    path("introspect/",
         oauth2_provider_views.IntrospectTokenView.as_view(),
         name="introspect"),
]

urlpatterns = base_urlpatterns + management_urlpatterns + oidc_urlpatterns

__all__ = [
    'app_name',
    'urlpatterns',
]
