"""
http request models
"""
from typing import Optional
from django.http import HttpRequest as _HttpRequest
from rollsocialnetwork.social.models import UserProfile
from rollsocialnetwork.phone_auth.models import OTPSecret

class HttpRequest(_HttpRequest):
    """
    http request model
    """
    user_profile: Optional[UserProfile]
    created_otp_secret: Optional[OTPSecret]
