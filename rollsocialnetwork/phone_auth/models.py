"""
phone auth models
"""
from django.db import models
from django.contrib.auth import get_user_model

from .utils import (
    fill_code,
    fill_valid_until,
    get_or_create_user,
)

class VerificationCode(models.Model):
    """
    Verification Code model
    """
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             blank=False)
    code = models.CharField(max_length=8,
                            default=fill_code,
                            blank=False,
                            editable=False)
    valid_until = models.DateTimeField(default=fill_valid_until,
                                       blank=False,
                                       editable=False)

    def __str__(self) -> str:
        return f"{self.user}'s verification code"

    @classmethod
    def request(cls, phone_number: str):
        """
        request verification code using phone number
        """
        user = get_or_create_user(phone_number)
        verification_code = cls(user=user)
        verification_code.save()
        return verification_code

    @classmethod
    def verify(cls, phone_number: str, code: str):
        """
        verify verification code using phone number and code
        """
        user = get_or_create_user(phone_number)
        try:
            verification_code = cls.objects.get(user=user, code=code)
        except cls.DoesNotExist:
            return None
        return verification_code
