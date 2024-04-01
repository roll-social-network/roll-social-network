"""
phone auth views
"""
from typing import Any
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
)
from django.views import View
from django.views.generic import (
    FormView,
    TemplateView,
)
from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import format_pn
from .forms import (
    LoginForm,
    VerifyVerificationCodeForm,
    VerifyOTPCodeForm,
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

    def form_valid(self, form: "LoginView") -> HttpResponse:
        return HttpResponseRedirect(self.get_success_url_from_form(form))

    def get_success_url_from_form(self, form: "LoginView") -> str:
        """
        get success url from form
        """
        pn = form.cleaned_data.get("phone_number")  # type: ignore[attr-defined]
        phone_number = format_pn(pn)
        has_otp_secret = OTPSecret.phone_number_has_otp_secret(phone_number)
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
