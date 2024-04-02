"""
phone auth backends
"""
from typing import (
    Dict,
    Optional,
)
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth import get_user_model
from rollsocialnetwork.http_request import HttpRequest
from .models import (
    VerificationCode,
    OTPSecret,
)

class GetUserMixin:  # pylint: disable=too-few-public-methods
    """
    Get User Mixin
    """
    def get_user(self, user_id):
        """
        get user
        """
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None

class PhoneAuthBackend(GetUserMixin,
                       BaseBackend):
    """
    phone auth backend class
    """
    def authenticate(self,  # type: ignore[override] # pylint: disable=W0221
                     request: HttpRequest,
                     phone_number: str,
                     code: str,
                     **kwargs: Dict) -> Optional[AbstractBaseUser]:
        verification_code = VerificationCode.verify(phone_number, code)
        if verification_code:
            return verification_code.user
        return None

class PhoneAuthOTPBackend(GetUserMixin,
                          BaseBackend):
    """
    phone auth backend class
    """
    def authenticate(self,  # type: ignore[override] # pylint: disable=W0221
                     request: HttpRequest,
                     phone_number: str,
                     otp_code: str,
                     **kwargs: Dict) -> AbstractBaseUser | None:
        otp_secret = OTPSecret.verify(phone_number, otp_code)
        if otp_secret:
            return otp_secret.user
        return None
