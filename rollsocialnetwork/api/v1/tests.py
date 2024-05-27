"""
api.v1 tests
"""
from unittest import mock
import phonenumbers
from django.test import (
    TestCase,
    RequestFactory,
)
from rest_framework.serializers import ValidationError
from rollsocialnetwork.tests_factory import (
    UserFactory,
    SiteFactory,
)
from .serializers import VerifyVerificationCodeSerializer
from .views import (
    SitesViewset,
    UsersViewset,
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
        self.factory = RequestFactory()
        self.site_factory = SiteFactory()

    def test_current(self):
        """
        current
        """
        request = self.factory.get('/api/v1/sites/current/')
        request.site = self.site_factory.create_site()
        response = SitesViewset(request=request,
                                format_kwarg={}).current(request)
        self.assertEqual(response.status_code, 200)

class UsersViewsetTestCase(TestCase):
    """
    UsersViewset test case
    """
    def setUp(self):
        self.factory = RequestFactory()
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
