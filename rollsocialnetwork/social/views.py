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
from django.core.paginator import (
    InvalidPage,
    Paginator,
    Page,
)
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from rollsocialnetwork.timeline.mixins import TimelineViewMixin
from .mixins import UserProfileRequiredMixin
from .models import UserProfile

class UserProfileDetailView(UserProfileRequiredMixin,
                            TimelineViewMixin,
                            DetailView):
    """
    user profile detail view
    """
    slug_field = "username"
    slug_url_kwarg = "username"
    page_kwarg = "page"
    slice_get_queryset_attr = "get_timeline_queryset"
    timeline_paginate_by = 10

    def get_queryset(self) -> QuerySet[UserProfile]:
        return UserProfile.objects.filter(site=self.request.site)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        timeline_paginator = self.get_timeline_paginator()
        timeline_page = self.get_timeline_page(timeline_paginator)
        context.update({
            "posts": timeline_page.object_list,
            "posts_page": timeline_page
        })
        return context

    def get_timeline_queryset(self):
        """
        get timeline queryset
        """
        return self.build_sliced_queryset(self.get_object().posts.all())

    def get_timeline_paginator(self):
        """
        get timeline paginator
        """
        return Paginator(self.get_timeline_queryset(), self.timeline_paginate_by)

    def get_timeline_page_number(self, timeline_paginator: Paginator) -> int:
        """
        get timeline page number
        """
        page = self.kwargs.get(self.page_kwarg) or self.request.GET.get(self.page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError as e:
            if page == "last":
                page_number = timeline_paginator.num_pages
            else:
                raise Http404(
                    _("Page is not “last”, nor can it be converted to an int.")
                ) from e
        return page_number

    def get_timeline_page(self, timeline_paginator: Paginator) -> Page:
        """
        get timeline page
        """
        timeline_page_number = self.get_timeline_page_number(timeline_paginator)
        try:
            return timeline_paginator.page(timeline_page_number)
        except InvalidPage as e:
            raise Http404(
                _("Invalid page (%(page_number)s): %(message)s")
                % {"page_number": timeline_page_number, "message": str(e)}
            ) from e

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
