"""
http request models
"""
from typing import Optional
from django.http import HttpRequest as _HttpRequest
from rollsocialnetwork.social.models import UserProfile

class HttpRequest(_HttpRequest):
    """
    http request model
    """
    user_profile: Optional[UserProfile]
