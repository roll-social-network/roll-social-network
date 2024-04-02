"""
phone auth models
"""
from typing import (
    Optional,
    Tuple,
)
from pyotp.totp import TOTP
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.sites.models import Site
from .sms_gateways import get_sms_gateway

from .utils import (
    fill_code,
    fill_valid_until,
    get_or_create_user,
    fill_otp_secret_value,
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
    attempts = models.PositiveIntegerField(default=settings.PHONE_AUTH_VERIFY_ATTEMPTS)

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
        sms_gateway = get_sms_gateway()
        sms_gateway.send(verification_code)
        return verification_code

    @classmethod
    def verify(cls, phone_number: str, code: str) -> Optional["VerificationCode"]:
        """
        verify verification code using phone number and code
        """
        user = get_or_create_user(phone_number)
        try:
            return cls.objects.get(user=user,
                                   code=code,
                                   valid_until__gte=timezone.now(),
                                   attempts__gt=0)
        except cls.DoesNotExist:
            cls.objects.filter(user=user,
                               valid_until__gte=timezone.now(),
                               attempts__gt=0).update(attempts=models.F('attempts') - 1)
            return None

class OTPSecret(models.Model):
    """
    OTP Secret model
    """

    user = models.OneToOneField(get_user_model(),
                                on_delete=models.CASCADE,
                                blank=False)
    value = models.CharField(max_length=32,
                             default=fill_otp_secret_value,
                             blank=False,
                             editable=False)
    valid_at = models.DateTimeField(null=True,
                                    blank=True)

    @classmethod
    def phone_number_has_valid_otp_secret(cls, phone_number: str) -> bool:
        """
        phone number has OTP secret
        """
        return OTPSecret.objects.filter(user__username=phone_number,
                                        valid_at__isnull=False).exists()

    @classmethod
    def create(cls, user: AbstractBaseUser) -> "OTPSecret":
        """
        create from user
        """
        return OTPSecret.objects.create(user=user)

    @classmethod
    def get_or_create(cls, user: AbstractBaseUser) -> Tuple["OTPSecret", bool]:
        """
        get or create from user
        """
        return OTPSecret.objects.get_or_create(user=user)

    @classmethod
    def verify(cls, phone_number: str, otp_code: str) -> Optional["OTPSecret"]:
        """
        verify OTP Code
        """
        try:
            otp_secret = OTPSecret.objects.get(user__username=phone_number)
            if otp_secret.totp.verify(otp_code):
                return otp_secret
            return None
        except OTPSecret.DoesNotExist:
            return None

    def __str__(self) -> str:
        """
        human-readable
        """
        return f"{self.user}'s OTP secret"

    @property
    def totp(self) -> TOTP:
        """
        TOTP instance
        """
        return TOTP(self.value)

    @property
    def uri(self) -> str:
        """
        uri for 2FA authentication apps
        """
        home_site = Site.objects.get(id=settings.HOME_SITE_ID)
        return self.totp.provisioning_uri(name=self.user.username,  # type: ignore[attr-defined]  # pylint: disable=no-member
                                          issuer_name=home_site.name)

    def validate(self, force_save=True):
        """
        validate
        """
        self.valid_at = timezone.now()
        if force_save:
            self.save()
