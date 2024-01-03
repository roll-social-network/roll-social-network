"""
social views
"""
from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    TemplateView,
    DetailView,
)
from django.views.generic.edit import CreateView
from django.contrib.auth.views import RedirectURLMixin  # type: ignore[attr-defined]
from .decorators import user_profile_required
from .models import UserProfile

@method_decorator([login_required, user_profile_required], name="dispatch")
class TimelineView(TemplateView):
    """
    timeline view
    """
    template_name = "social/timeline.html"

@method_decorator([login_required, user_profile_required], name="dispatch")
class UserProfileDetailView(DetailView):
    """
    user profile detail view
    """
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_queryset(self) -> QuerySet[Any]:
        return UserProfile.objects.filter(site=self.request.site)

@method_decorator(login_required, name="dispatch")
class UserProfileCreateView(RedirectURLMixin, CreateView):
    """
    user profile create view
    """
    model = UserProfile
    fields = ["username"]

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        form.instance.site = self.request.site
        return super().form_valid(form)
