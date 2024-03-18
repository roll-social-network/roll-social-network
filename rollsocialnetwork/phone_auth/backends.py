"""
phone auth backends
"""
from typing import Any
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest
from django.contrib.auth import get_user_model
from .models import VerificationCode

class PhoneAuthBackend(BaseBackend):
    """
    phone auth backend class
    """
    def authenticate(self,  # type: ignore[override] pylint: disable=W0221
                     request: HttpRequest,
                     phone_number: str,
                     code: str,
                     **kwargs: Any) -> AbstractBaseUser | None:
        verification_code = VerificationCode.verify(phone_number, code)
        if verification_code:
            return verification_code.user
        return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
