"""
phone auth views
"""
from typing import Any, Optional
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseBadRequest,
)
from django.views import View
from django.views.generic import FormView
from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import (
    reverse,
    reverse_lazy as _reverse,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from rollsocialnetwork.http_request import HttpRequest
from .utils import format_pn
from .forms import (
    LoginForm,
    VerifyVerificationCodeForm,
    VerifyOTPCodeForm,
    ValidateOTPSecretForm,
)
from .models import (
    VerificationCode,
    OTPSecret,
)

class LoginView(FormView):
    """
    login view
    """

    form_class = LoginForm
    template_name = "phone_auth/login_form.html"

    def get_initial(self) -> dict[str, Any]:
        return self.request.GET.dict()

    def form_valid(self, form: "LoginForm") -> HttpResponse:
        return HttpResponseRedirect(self.get_verify_url(form))

    def get_verify_url(self, form: "LoginForm") -> str:
        """
        get verify url
        """
        pn = form.cleaned_data.get("phone_number")  # type: ignore[attr-defined]
        phone_number = format_pn(pn)
        has_otp_secret = OTPSecret.phone_number_has_valid_otp_secret(phone_number)
        if has_otp_secret:
            return reverse("verify-otp-code",
                           kwargs={"phone_number": phone_number})
        return reverse("request-verification-code",
                       kwargs={"phone_number": phone_number})

class RequestVerificationCodeView(View):
    """
    request verification code view
    """

    def get(self, request, phone_number=None):
        """
        get
        """
        VerificationCode.request(phone_number)
        return HttpResponseRedirect(reverse("verify-verification-code",
                                            kwargs={"phone_number": phone_number}))

class VerifyVerificationCodeView(AuthLoginView):
    """
    verify verification code view
    """

    template_name = "phone_auth/verify_verification_code_form.html"
    form_class = VerifyVerificationCodeForm

    def get_initial(self) -> dict[str, Any]:
        return self.kwargs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            "phone_number": self.kwargs.get("phone_number")
        })
        return context

class VerifyOTPCodeView(AuthLoginView):
    """
    verify verification code view
    """

    template_name = "phone_auth/verify_otp_code_form.html"
    form_class = VerifyOTPCodeForm

    def get_initial(self) -> dict[str, Any]:
        return self.kwargs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        request_url = reverse("request-verification-code",
                              kwargs={"phone_number": self.kwargs.get("phone_number")})
        context.update({
            "phone_number": self.kwargs.get("phone_number"),
            "send_via_sms_url": request_url
        })
        return context

class ValidateOTPSecretView(LoginRequiredMixin,
                            FormView):
    """
    Validate OTP Secret view
    """

    template_name = "phone_auth/validate_otp_secret_form.html"
    form_class = ValidateOTPSecretForm
    success_url = _reverse("timeline")

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.otp_secret: Optional[OTPSecret] = None

    def setup(self, request: HttpRequest, *args, **kwargs):  # type: ignore[override]
        self.otp_secret, _ = OTPSecret.get_or_create(request.user)
        return super().setup(request, *args, **kwargs)

    def dispatch(self,
                 request: HttpRequest,  # type: ignore[override]
                 *args,
                 **kwargs) -> HttpResponse:
        if not self.otp_secret or self.otp_secret.valid_at:
            return HttpResponseBadRequest()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({ "otp_secret": self.otp_secret })
        return context

    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs.update({ "otp_secret": self.otp_secret })
        return kwargs

    def form_valid(self, form: "ValidateOTPSecretForm") -> HttpResponse:
        if self.otp_secret:
            self.otp_secret.validate()
        return super().form_valid(form)
