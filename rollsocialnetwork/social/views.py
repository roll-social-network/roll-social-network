"""
social views
"""
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import RedirectURLMixin  # type: ignore[attr-defined]
from .mixins import UserProfileRequiredMixin
from .models import UserProfile

class UserProfileDetailView(UserProfileRequiredMixin,
                            DetailView):
    """
    user profile detail view
    """
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_queryset(self) -> QuerySet[UserProfile]:
        return UserProfile.objects.filter(site=self.request.site)

@method_decorator(login_required, name="dispatch")
class UserProfileCreateView(RedirectURLMixin,
                            CreateView):
    """
    user profile create view
    """
    model = UserProfile
    fields = ["username"]

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        form.instance.site = self.request.site
        return super().form_valid(form)
