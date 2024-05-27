"""
timeline views
"""
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
)
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.forms.models import BaseModelForm
from django.db.models.query import QuerySet
from django.conf import settings
from rollsocialnetwork.http_request import HttpRequest
from rollsocialnetwork.social.mixins import UserProfileRequiredMixin
from .models import Post
from .mixins import TimelineViewMixin

class TimelineView(UserProfileRequiredMixin,  # pylint: disable=R0901
                   TimelineViewMixin,
                   ListView):
    """
    timeline view
    """
    model = Post
    ordering = ["-created_at"]
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Post]:
        """
        get queryset
        """
        queryset = super().get_queryset()
        if not self.is_home_site():
            queryset = queryset.filter(  # type: ignore[attr-defined]
                user_profile__site=self.request.site)
        return self.build_sliced_queryset(queryset)

    def is_home_site(self):
        """
        is home site
        """
        return self.request.site.id == settings.HOME_SITE_ID

    def get_template_names(self):
        """
        get template names
        """
        if self.request.headers.get("AJAX-Request") == 'true':
            return ["timeline/post_list_ajax.html"]
        return super().get_template_names()

class PostCreateView(UserProfileRequiredMixin,
                     CreateView):
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

class PostLikeDislikeView(UserProfileRequiredMixin,
                          DetailView):
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
