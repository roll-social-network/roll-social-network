"""
oauth2 views
"""
from django.conf import settings
from django.views.generic import RedirectView

class RedirectToSSOAppAuthorizeURL(RedirectView):
    """
    redirect to sso app authorize url
    """
    url = settings.SSO_APP_AUTHORIZE_URL
    query_string = True
