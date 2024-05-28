"""
api.v1 tests
"""
from unittest import mock
import phonenumbers
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.serializers import ValidationError
from rest_framework import status
from oauth2_provider.exceptions import OAuthToolkitError  # type: ignore[import-untyped]
from oauthlib.oauth2 import AccessDeniedError
from rollsocialnetwork.phone_auth.models import VerificationCode
from rollsocialnetwork.tests_factory import (
    OAuth2ApplicationFactory,
    OAuth2AccessTokenFactory,
    UserFactory,
    SiteFactory,
)
from .serializers import VerifyVerificationCodeSerializer
from .views import (
    SitesViewset,
    UsersViewset,
    LoginView,
    RequestVerificationCodeView,
    VerifyVerificationCodeView,
    OAuth2AuthorizeView,
)

PHONE_NUMBER = "+55 11 98070-6050"
CODE = "1234"

class VerifyVerificationCodeSerializerTestCase(TestCase):
    """
    VerifyVerificationCodeSerializer test case
    """
    def setUp(self):
        self.user_factory = UserFactory()

    @mock.patch("rollsocialnetwork.api.v1.serializers.authenticate")
    def test_validate_ok(self, authenticate_mock):
        """
        .validate ok
        """
        user = self.user_factory.create_user()
        authenticate_mock.return_value = user
        serializer = VerifyVerificationCodeSerializer()
        attrs = {
            "phone_number": phonenumbers.parse(PHONE_NUMBER, None),
            "code": CODE
        }
        result = serializer.validate(attrs)
        self.assertIn("user", result.keys())
        self.assertEqual(result["user"], user)

    @mock.patch("rollsocialnetwork.api.v1.serializers.authenticate")
    def test_validate_invalid_code(self, authenticate_mock):
        """
        .validate invalid code
        """
        authenticate_mock.return_value = None
        serializer = VerifyVerificationCodeSerializer()
        attrs = {
            "phone_number": phonenumbers.parse(PHONE_NUMBER, None),
            "code": CODE
        }
        with self.assertRaises(ValidationError):
            serializer.validate(attrs)

    def test_validate_phone_number_code_required(self):
        """
        .validate phone_number and code is required
        """
        serializer = VerifyVerificationCodeSerializer()
        attrs = {}
        with self.assertRaises(ValidationError):
            serializer.validate(attrs)

class SitesViewsetTestCase(TestCase):
    """
    SitesViewset test case
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.site_factory = SiteFactory()

    def test_current(self):
        """
        current
        """
        request = self.factory.get('/api/v1/sites/current/')
        request.site = self.site_factory.create_site()
        response = SitesViewset(request=request,
                                format_kwarg={}).current(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UsersViewsetTestCase(TestCase):
    """
    UsersViewset test case
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_factory = UserFactory()

    def test_current(self):
        """
        current
        """
        request = self.factory.get('/api/v1/users/current/')
        request.user = self.user_factory.create_user()
        response = UsersViewset(request=request,
                                format_kwarg={}).current(request)
        self.assertEqual(response.status_code, 200)

class LoginViewTestCase(TestCase):
    """
    LoginView test case
    """
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_ok(self):
        """
        ok
        """
        request = self.factory.post('/api/v1/login/', data={ "phone_number": PHONE_NUMBER })
        response = LoginView(request=request).as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class RequestVerificationCodeViewTestCase(TestCase):
    """
    RequestVerificationCodeView test case
    """
    def setUp(self):
        self.factory = APIRequestFactory()

    @mock.patch.object(VerificationCode, "request")
    def test_ok(self, request_mock):
        """
        ok
        """
        request = self.factory.post('/api/v1/request-verification-code/',
                                    data={ "phone_number": PHONE_NUMBER })
        response = RequestVerificationCodeView(request=request).as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        request_mock.assert_called()

class VerifyVerificationCodeViewTestCase(TestCase):
    """
    VerifyVerificationCodeView test case
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_factory = UserFactory()

    @mock.patch.object(VerifyVerificationCodeSerializer, "validate")
    def test_ok(self, validate_mock):
        """
        ok
        """
        data = {
            "phone_number": PHONE_NUMBER,
            "code": CODE
        }
        validate_mock.return_value = { **data, **{ "user": self.user_factory.create_user() } }
        request = self.factory.post('/api/v1/verify-verification-code/',
                                    data=data)
        response = VerifyVerificationCodeView(request=request).as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class OAuth2AuthorizeViewTestCase(TestCase):
    """
    OAuth2AuthorizeView test case
    """
    def setUp(self):
        user_factory = UserFactory()
        self.user = user_factory.create_user()
        self.factory = APIRequestFactory()
        self.oauth2_application_factory = OAuth2ApplicationFactory()
        self.oauth2_access_token_factory = OAuth2AccessTokenFactory()

    @mock.patch.object(OAuth2AuthorizeView, "validate_authorization_request")
    def test_get_ok(self, validate_authorization_request_mock):
        """
        get ok
        """
        redirect_uri = "http://testexample/social/complete/roll/"
        oauth2_app = self.oauth2_application_factory.create_oauth2_application(
            redirect_uris=redirect_uri
        )
        scopes = ["openid"]
        credentials = {
            "client_id": oauth2_app.client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code"
        }
        validate_authorization_request_mock.return_value = (scopes, credentials,)
        request = self.factory.get('/api/v1/oauth2/authorize/')
        request.user = self.user
        response = OAuth2AuthorizeView(request=request).as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @mock.patch.object(OAuth2AuthorizeView, "validate_authorization_request")
    def test_get_validate_raise_oauth_toolkit_error(self, validate_authorization_request_mock):
        """
        get raise OAuth2AuthorizeView
        """
        validate_authorization_request_mock.side_effect = OAuthToolkitError(AccessDeniedError())
        request = self.factory.get('/api/v1/oauth2/authorize/')
        request.user = self.user
        response = OAuth2AuthorizeView(request=request).as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch.object(OAuth2AuthorizeView, "validate_authorization_request")
    def test_post_ok(self, validate_authorization_request_mock):
        """
        post ok
        """
        redirect_uri = "http://testexample/social/complete/roll/"
        oauth2_app = self.oauth2_application_factory.create_oauth2_application(
            redirect_uris=redirect_uri
        )
        scopes = ["openid"]
        credentials = {
            "client_id": oauth2_app.client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code"
        }
        validate_authorization_request_mock.return_value = (scopes, credentials,)
        request = self.factory.post('/api/v1/oauth2/authorize/')
        request.user = self.user
        response = OAuth2AuthorizeView(request=request).as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @mock.patch.object(OAuth2AuthorizeView, "validate_authorization_request")
    def test_post_prompt_auto(self, validate_authorization_request_mock):
        """
        post prompt auto
        """
        redirect_uri = "http://testexample/social/complete/roll/"
        oauth2_app = self.oauth2_application_factory.create_oauth2_application(
            redirect_uris=redirect_uri
        )
        scopes = ["openid"]
        credentials = {
            "client_id": oauth2_app.client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "approval_prompt": "auto"
        }
        validate_authorization_request_mock.return_value = (scopes, credentials,)
        request = self.factory.post('/api/v1/oauth2/authorize/')
        request.user = self.user
        response = OAuth2AuthorizeView(request=request).as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.oauth2_access_token_factory.create_oauth2_access_token(user=self.user,
                                                                    application=oauth2_app,
                                                                    scope=' '.join(scopes))
        request = self.factory.post('/api/v1/oauth2/authorize/')
        request.user = self.user
        response = OAuth2AuthorizeView(request=request).as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
