"""
api.v1 tests
"""
from unittest import mock
import phonenumbers
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.serializers import ValidationError
from rest_framework import status
from rollsocialnetwork.phone_auth.models import VerificationCode
from rollsocialnetwork.tests_factory import (
    UserFactory,
    SiteFactory,
)
from .serializers import VerifyVerificationCodeSerializer
from .views import (
    SitesViewset,
    UsersViewset,
    LoginView,
    RequestVerificationCodeView,
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
