"""
Opener Callback

Flux to interact with popups openers.

1. Opener open Action View popup.
1. Action View redirect to OpenerCallbackView.
1. OpenerCallbackView sends callback menssage to origin.
"""

from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import TemplateView

class OpenerCallbackRedirectURLMixin:  # pylint: disable=R0903
    """
    Opener Callback Redirect URL Mixin
    """
    MESSAGE_FIELD_NAME = "ocm"
    ORIGIN_FIELD_NAME = "oco"

    def get_redirect_url(self):
        """
        get redirect url

        overrides get_redirect_url() to redirect to open callback URL when message field is setted
        """
        message = self.request.GET.get(self.__class__.MESSAGE_FIELD_NAME)
        if not message:
            return super().get_redirect_url()
        url = reverse("opener_callback")
        qs = {"message": message}
        origin = self.request.GET.get(self.__class__.ORIGIN_FIELD_NAME)
        if origin:
            qs.update({"origin": origin})
        return f"{url}?{urlencode(qs)}"

class OpenerCallbackView(TemplateView):
    """
    Opener Callback View
    """
    template_name = "opener_callback.html"
