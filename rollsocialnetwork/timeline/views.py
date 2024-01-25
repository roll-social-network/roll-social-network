"""
timeline views
"""
from django.http import HttpResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.forms.models import BaseModelForm
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
