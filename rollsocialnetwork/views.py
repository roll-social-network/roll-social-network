"""
rollsocialnetwork views
"""
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseRedirect
)
from django.views.generic import View
from django.conf import settings
from django.contrib.auth import logout

class LogoutView(View):
    """
    logout view
    """
    def get(self, request):
        """
        get
        """
        logout(request)
        return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)

class NginxAccelRedirectView(View):
    """
    NGINX Accel Redirect view

    Uses X-Accel to protected all media resources.
    https://www.nginx.com/resources/wiki/start/topics/examples/x-accel/
    """

    def get(self, request, path):
        """
        get method
        """
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        response = HttpResponse(
            headers={
                "X-Accel-Redirect": f"{settings.NGINX_ACCEL_REDIRECT_INTERNAL_LOCATION}{path}"
            },
            content_type=""
        )
        return response
