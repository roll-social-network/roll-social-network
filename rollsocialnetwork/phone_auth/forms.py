"""
phone auth forms
"""
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField  # type: ignore[import-untyped]
from .utils import format_pn

class RequestVerificationCodeForm(forms.Form):
    """
    request verification code form
    """
    phone = PhoneNumberField()

class VerifyVerificationCodeForm(forms.Form):
    """
    verify verification code form
    """
    phone = PhoneNumberField()
    code = forms.CharField(max_length=8)

    error_messages = {
        "invalid_login": _("Please enter a correct verification code"),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, *args, request=None, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        pn = self.cleaned_data.get("phone")
        phone_number = format_pn(pn)
        code = self.cleaned_data.get("code")
        if phone_number is not None and code:
            self.user_cache = authenticate(self.request,
                                           phone_number=phone_number,
                                           code=code)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

    def get_user(self):
        """
        get user
        """
        return self.user_cache

    def get_invalid_login_error(self):
        """
        get invalid login error
        """
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
        )

    def confirm_login_allowed(self, user):
        """
        check if user is activated
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )
