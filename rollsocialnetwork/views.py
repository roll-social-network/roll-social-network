"""
rollsocialnetwork views
"""
from typing import Dict, List
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseRedirect
)
from django.views.generic import (
    View,
    TemplateView,
)
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.sites.models import Site
from django.db.models import QuerySet

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

class HomeView(TemplateView):
    """
    home view
    """

    @property
    def is_home_site(self) -> bool:
        """
        is home site?
        """
        return self.request.site.id == settings.HOME_SITE_ID  # type: ignore[attr-defined]

    def get_template_names(self) -> List[str]:
        if self.is_home_site:
            return ["home_site.html"]
        return ["home.html"]

    def get_context_data(self, **kwargs) -> Dict:
        context_data = super().get_context_data(**kwargs)
        if self.is_home_site:
            context_data.update({
                "popular": get_popular_sites()
            })
        return context_data

def get_popular_sites() -> QuerySet[Site]:
    """
    get popular sites
    """
    return Site.objects.exclude(id=settings.HOME_SITE_ID)
