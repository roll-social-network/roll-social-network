"""
phone auth models
"""
import random
import string
from datetime import timedelta
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone

def fill_code() -> str:
    """
    fill code field considering PHONE_AUTH_VALIDATION_CODE_LENGTH setting
    """
    return ''.join(random.choice(string.digits) for _ in range(
        settings.PHONE_AUTH_VALIDATION_CODE_LENGTH))

def fill_valid_until():
    """
    fill valid until field considering PHONE_AUTH_VALIDATION_CODE_TTL setting
    """
    return timezone.now() + timedelta(minutes=settings.PHONE_AUTH_VALIDATION_CODE_TTL)

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
