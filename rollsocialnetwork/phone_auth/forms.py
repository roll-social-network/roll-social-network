"""
phone auth forms
"""
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField  # type: ignore[import-untyped]
from phonenumber_field.widgets import (  # type: ignore[import-untyped]
    RegionalPhoneNumberWidget,
    PhoneNumberPrefixWidget,
)

from .models import OTPSecret
from .utils import format_pn

PHONE_NUMBER_READYONLY_FIELD = PhoneNumberField(label=_('phone number'),
                                                widget=RegionalPhoneNumberWidget(
                                                    attrs={"readonly": True}))

class LoginForm(forms.Form):
    """
    login form
    """
    phone_number = PhoneNumberField(label=_("phone number"),
                                    help_text=_("select your country prefix and fill with your "
                                                "phone number"),
                                    widget=PhoneNumberPrefixWidget(
                                        country_attrs={"data-prefix-phone-number": True}))

class VerifyCodeFormMixin:
    """
    Verify Code Form Mixin
    """

    authenticate_fn = authenticate

    def __init__(self, *args, request=None, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        """
        clean data
        """
        pn = self.cleaned_data.get("phone_number")
        phone_number = format_pn(pn)
        code = self.cleaned_data.get("code")
        if phone_number is not None and code:
            self.user_cache = self.call_authenticate(phone_number, code)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

    def call_authenticate(self, phone_number, code):
        """
        call_authenticate
        """
        raise NotImplementedError()

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

class VerifyVerificationCodeForm(VerifyCodeFormMixin,
                                 forms.Form):
    """
    verify verification code form
    """

    phone_number = PHONE_NUMBER_READYONLY_FIELD
    code = forms.CharField(max_length=8,
                           label=_("code"),
                           help_text=_("sent via SMS"))

    error_messages = {
        "invalid_login": _("please enter a correct verification code"),
        "inactive": _("this account is inactive."),
    }

    def call_authenticate(self, phone_number, code):
        return self.authenticate_fn(phone_number=phone_number,
                                    code=code)

class VerifyOTPCodeForm(VerifyCodeFormMixin,
                        forms.Form):
    """
    verify OTP code form
    """

    phone_number = PHONE_NUMBER_READYONLY_FIELD
    code = forms.IntegerField(label=_("code"),
                              help_text=_("generated by 2FA authentication apps"),
                              min_value=1)

    error_messages = {
        "invalid_login": _("please enter a correct OTP code"),
        "inactive": _("this account is inactive."),
    }

    def call_authenticate(self, phone_number, code):
        return self.authenticate_fn(phone_number=phone_number,
                                    otp_code=code)

class ValidateOTPSecretForm(forms.Form):
    """
    validate OTP secret form
    """
    code = forms.IntegerField(label=_("code"),
                              help_text=_("generated by 2FA authentication apps"),
                              min_value=1)

    def __init__(self, *args, otp_secret: OTPSecret, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.otp_secret = otp_secret

    def clean_code(self):
        """
        clean code field
        """
        code = self.cleaned_data.get("code")
        if not self.otp_secret.totp.verify(code):
            raise forms.ValidationError(_("invalid or expired OTP code"))
        return code
