"""
rollsocialnetwork views
"""
from typing import (
    Dict,
    List
)
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseRedirect
)
from django.views.generic import (
    View,
    TemplateView,
    ListView,
    CreateView,
    RedirectView
)
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.sites.models import Site
from django.db.models import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .forms import RollForm
from .utils import get_popular_rolls

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
                "popular": get_popular_rolls()[:6]
            })
        return context_data

class RollsView(ListView):
    """
    rolls view
    """

    model = Site
    paginate_by = 12

    def get_queryset(self) -> QuerySet[Site]:
        return get_popular_rolls()

class CreateRollView(LoginRequiredMixin,
                     CreateView):
    """
    create roll view
    """
    model = Site
    form_class = RollForm

    def get_success_url(self):
        scheme = settings.OVERRIDE_SCHEME or self.request.scheme
        return f"{scheme}://{self.object.domain}"

class LoginView(RedirectView):
    """
    login view
    """
    def get_redirect_url(self, *args, **kwargs) -> str:
        url = reverse("phoneauth:login")
        qs = self.request.META.get("QUERY_STRING")
        if qs:
            url = f"{url}?{qs}"
        return url
