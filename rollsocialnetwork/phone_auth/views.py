"""
phone auth views
"""
from typing import Any
from urllib.parse import urlencode
from django.views.generic import (
    FormView,
    TemplateView,
)
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import format_pn
from .forms import (
    RequestVerificationCodeForm,
    VerifyVerificationCodeForm,
)
from .models import (
    VerificationCode,
    OTPSecret,
)

class RequestVerificationCodeView(FormView):
    """
    request verification code view
    """
    template_name = "phone_auth/request_form.html"
    form_class = RequestVerificationCodeForm
    success_url = reverse_lazy("verify-verification-code")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._phone_number = None

    def form_valid(self, form):
        pn = form.cleaned_data.get("phone")
        self._phone_number = format_pn(pn)
        VerificationCode.request(self._phone_number)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        success_url = super().get_success_url()
        params = {
            **{"phone": self._phone_number},
            **self.request.GET.dict(),
        }
        return f"{success_url}?{urlencode(params)}"

class VerifyVerificationCodeView(LoginView):
    """
    verify verification code view
    """
    template_name = "phone_auth/verify_verification_code_form.html"
    form_class = VerifyVerificationCodeForm

    def get_initial(self) -> dict[str, Any]:
        return self.request.GET.dict()

class ShowOTPSecretView(LoginRequiredMixin,
                        TemplateView):
    """
    Show OTP Secret view
    """

    template_name = "phone_auth/show_otp_secret.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        otp_secret, _ = OTPSecret.get_or_create(self.request.user)  # type: ignore[arg-type]
        context.update({
            "otp_secret": otp_secret
        })
        return context
