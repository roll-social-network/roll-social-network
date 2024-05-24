"""
api.v1 serializers
"""
from typing import Optional
from rest_framework import serializers
from django.contrib.sites.models import Site
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.serializerfields import PhoneNumberField  # type: ignore[import-untyped]
from oauth2_provider.settings import oauth2_settings  # type: ignore[import-untyped]
from oauth2_provider.models import get_application_model  # type: ignore[import-untyped]
from rollsocialnetwork.phone_auth.utils import format_pn

UserModel = get_user_model()

class SiteSerializer(serializers.ModelSerializer):
    """
    site serializer
    """
    class Meta:
        model = Site
        fields = [
            "domain",
            "name"
        ]

class UserSerializer(serializers.ModelSerializer):
    """
    user serializer
    """
    class Meta:
        model = UserModel
        fields = [
            "username",
            "full_name",
            "date_joined",
        ]

    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj: AbstractUser) -> Optional[str]:
        """
        get full name
        """
        return obj.get_full_name() or None

class LoginSerializer(serializers.Serializer):
    """
    login serializer
    """
    phone_number = PhoneNumberField()

    def create(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

class RequestVerificationCodeSerializer(serializers.Serializer):
    """
    request verification code serializer
    """
    phone_number = PhoneNumberField()

    def create(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

class VerifyVerificationCodeSerializer(serializers.Serializer):
    """
    verify verification code serializer
    """
    phone_number = PhoneNumberField()
    code = serializers.CharField()

    def validate(self, attrs):
        pn = attrs.get("phone_number")
        phone_number = format_pn(pn)
        code = attrs.get("code")
        if phone_number and code:
            user = authenticate(request=self.context.get("request"),
                                phone_number=phone_number,
                                code=code)
            if user:
                attrs["user"] = user
                return attrs
            msg = _("please enter a correct verification code")
            raise serializers.ValidationError(msg, code="authorization")
        msg = _("Must include phone_number and code.")
        raise serializers.ValidationError(msg, code="authorization")

    def create(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

class OAuth2ApplicationSerializer(serializers.ModelSerializer):
    """
    oauth2 application serializer
    """
    class Meta:
        model = get_application_model()
        fields = [
            "client_id",
            "name",
            "skip_authorization",
        ]

class OAuth2AuthorizeSerializer(serializers.Serializer):
    """
    oauth2 authorize serializer
    """
    approval_prompt = serializers.CharField(default=oauth2_settings.REQUEST_APPROVAL_PROMPT)
    redirect_uri = serializers.CharField()
    response_type = serializers.CharField()
    state = serializers.CharField(required=False)
    code_challenge = serializers.CharField(required=False)
    code_challenge_method = serializers.CharField(required=False)
    nonce = serializers.CharField(required=False)
    claims = serializers.DictField(required=False)
    scopes = serializers.DictField()
    application = OAuth2ApplicationSerializer()

    def create(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass
