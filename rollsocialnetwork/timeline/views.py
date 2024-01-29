"""
timeline views
"""
from typing import (
    Any,
    Optional,
)
from django.http import HttpResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.forms.models import BaseModelForm
from django.db.models.query import QuerySet
from rollsocialnetwork.http_request import HttpRequest
from rollsocialnetwork.social.decorators import user_profile_required
from .models import Post

@method_decorator([login_required, user_profile_required], name="dispatch")
class TimelineView(ListView):
    """
    timeline view
    """
    model = Post
    ordering = ["-created_at"]
    paginate_by = 10
    slice_kwarg = "slice"

    def _retrive_slice_value(self) -> Optional[str]:
        qs = self.get_queryset()
        if qs.count() == 0:
            return None
        return str(qs[0].pk)

    def fill_slice_value(self) -> Optional[str]:
        """
        fill slice value
        """
        return self.get_slice_value() or self._retrive_slice_value()

    def get_slice_value(self) -> Optional[str]:
        """
        get slice value
        """
        return self.request.GET.get(self.slice_kwarg)

    def fill_has_new_post_out_slice(self) -> bool:
        """
        fill has new post out slice
        """
        slice_value = self.get_slice_value()
        if not slice_value:
            return False
        return self.model.objects.filter(pk__gt=slice_value).count() > 0

    def get_queryset(self) -> QuerySet[Post]:
        queryset = super().get_queryset()
        slice_value = self.get_slice_value()
        if not slice_value:
            return queryset
        return queryset.filter(pk__lte=slice_value)

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            "slice_kwarg": self.slice_kwarg,
            "slice": self.fill_slice_value(),
            "has_new_post_out_slice": self.fill_has_new_post_out_slice(),
        })
        return context_data

@method_decorator([login_required, user_profile_required], name="dispatch")
class PostCreateView(CreateView):
    """
    post create view
    """
    model = Post
    fields = ["photo"]
    request: HttpRequest

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user_profile = self.request.user_profile
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('timeline')
