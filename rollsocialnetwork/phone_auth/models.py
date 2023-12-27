"""
phone auth models
"""
from django.db import models
from django.contrib.auth import get_user_model

from .utils import (
    fill_code,
    fill_valid_until,
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
