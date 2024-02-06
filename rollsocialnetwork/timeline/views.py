"""
timeline views
"""
from typing import (
    Any,
    Optional,
)
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
)
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
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
        return reverse("timeline")

@method_decorator([login_required, user_profile_required], name="dispatch")
class PostLikeDislikeView(DetailView):
    """
    like dislike view
    """
    model = Post

    def get_queryset(self) -> QuerySet[Post]:
        return Post.objects.filter(user_profile__site=self.request.site)

    def get(self, request: HttpRequest, *args, **kwargs):  # type: ignore[override]
        post: Post = self.get_object()  # type: ignore[assignment]
        user_profile = request.user_profile
        if not user_profile:
            return HttpResponseBadRequest()
        like = post.like_dislike(user_profile)
        success_url = self.get_success_url()
        action_component = request.headers.get("Action-Component")
        if action_component == "like-dislike":
            status_code = 201 if like else 204
            return HttpResponse(status=status_code)
        return HttpResponseRedirect(success_url)

    def get_success_url(self) -> str:
        """
        get success url
        """
        post_pk = self.kwargs.get(self.pk_url_kwarg)
        reverse_timeline = reverse("timeline")
        return f"{reverse_timeline}#post-{post_pk}"
