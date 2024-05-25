"""
api.vi views
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.utils import timezone
from oauth2_provider.exceptions import OAuthToolkitError  # type: ignore[import-untyped]
from oauth2_provider.views.mixins import OAuthLibMixin  # type: ignore[import-untyped]
from oauth2_provider.scopes import get_scopes_backend  # type: ignore[import-untyped]
from oauth2_provider.models import (  # type: ignore[import-untyped]
    get_application_model,
    get_access_token_model,
)
from rollsocialnetwork.phone_auth.login_methods import available_methods
from rollsocialnetwork.phone_auth.models import VerificationCode
from rollsocialnetwork.phone_auth.utils import format_pn
from .serializers import (
    SiteSerializer,
    UserSerializer,
    LoginSerializer,
    RequestVerificationCodeSerializer,
    VerifyVerificationCodeSerializer,
    OAuth2AuthorizeSerializer,
)

class SitesViewset(viewsets.ReadOnlyModelViewSet):  # pylint: disable=R0901
    """
    sites viewset
    """
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

    @action(detail=False)
    def current(self, request: Request):
        """
        current
        """
        serializer = self.get_serializer(request.site)
        return Response(serializer.data)

class UsersViewset(RetrieveModelMixin,
                   GenericViewSet):
    """
    users viewset
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    @action(detail=False, permission_classes=[IsAuthenticated])
    def current(self, request: Request):
        """
        current
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class LoginView(APIView):
    """
    login view
    """
    def post(self, request: Request):
        """
        login
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pn = serializer.validated_data.get("phone_number")
        phone_number = format_pn(pn)
        return Response(
            {
                "available_methods": available_methods(phone_number)
            },
            status=status.HTTP_200_OK
        )

class RequestVerificationCodeView(APIView):
    """
    request verification code
    """
    def post(self, request: Request):
        """
        request
        """
        serializer = RequestVerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pn = serializer.validated_data.get("phone_number")
        phone_number = format_pn(pn)
        VerificationCode.request(phone_number)
        return Response(status=status.HTTP_202_ACCEPTED)

class VerifyVerificationCodeView(APIView):
    """
    verify verification code
    """
    def post(self, request: Request):
        """
        verify
        """
        serializer = VerifyVerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.pk,
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)

class OAuth2AuthorizeView(OAuthLibMixin,
                          APIView):
    """
    OAuth2 authorize view
    """
    def api_error_response(self, error: OAuthToolkitError):
        """
        error response
        """
        return Response(
            { "message": error.oauthlib_error.description },
            status=error.oauthlib_error.status_code
        )

    def get(self, request: Request):
        """
        get authorize
        """
        try:
            scopes, credentials = self.validate_authorization_request(request)
        except OAuthToolkitError as error:
            return self.api_error_response(error)
        all_scopes = get_scopes_backend().get_all_scopes()
        application = get_application_model().objects.get(client_id=credentials["client_id"])
        instance = {
            "redirect_uri": credentials["redirect_uri"],
            "response_type": credentials["response_type"],
            "state": credentials.get("state"),
            "code_challenge": credentials.get("code_challenge"),
            "code_challenge_method": credentials.get("code_challenge_method"),
            "nonce": credentials.get("nonce"),
            "scopes": { scope: all_scopes[scope] for scope in scopes },
            "application": application
        }
        approval_prompt = request.GET.get("approval_prompt")
        if approval_prompt:
            instance["approval_prompt"] = approval_prompt
        claims = credentials.get("claims")
        if claims:
            instance["claims"] = claims
        serializer = OAuth2AuthorizeSerializer(instance)
        return Response(serializer.data)

    def post(self, request: Request):
        """
        allow
        """
        try:
            scopes, credentials = self.validate_authorization_request(request)
            application = get_application_model().objects.get(client_id=credentials["client_id"])
            create_authorization_kwargs = {
                "request": request,
                "scopes": " ".join(scopes),
                "credentials": credentials,
                "allow": True,
            }
            approval_prompt = request.GET.get("approval_prompt")
            if approval_prompt != "auto":
                uri, _, _, _ = self.create_authorization_response(**create_authorization_kwargs)
                return Response({ "uri": uri })
            tokens = get_access_token_model().objects.filter(user=request.user,
                                                             application=application,
                                                             expires__gt=timezone.now()).all()
            for token in tokens:
                if token.allow_scopes(scopes):
                    uri, _, _, _ = self.create_authorization_response(**create_authorization_kwargs)
                    return Response({ "uri": uri })
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except OAuthToolkitError as error:
            return self.api_error_response(error)
