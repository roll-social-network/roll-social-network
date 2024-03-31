"""
phone auth utils
"""
import random
import string
from datetime import timedelta
import phonenumbers
import pyotp
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser

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

def format_pn(pn: phonenumbers.PhoneNumber) -> str:
    """
    format PhoneNumber object to string
    """
    return phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164)

def normalize_phone_number(phone_number: str) -> str:
    """
    normalize phone number
    """
    pn = phonenumbers.parse(phone_number, None)
    return format_pn(pn)

def get_or_create_user(phone_number: str) -> AbstractBaseUser:
    """
    get or create user using phone number
    """
    cleaned_phone_number = normalize_phone_number(phone_number)
    user_model = get_user_model()
    try:
        user = user_model.objects.get(**{
            user_model.USERNAME_FIELD: cleaned_phone_number, # type: ignore[attr-defined]
        })
    except user_model.DoesNotExist:
        user = user_model(**{
            user_model.USERNAME_FIELD: cleaned_phone_number, # type: ignore[attr-defined]
        })
        user.save()
    return user

def fill_otp_secret_value() -> str:
    """
    fill OTPSecret value
    """
    return pyotp.random_base32()
