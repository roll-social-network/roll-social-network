"""
api.v1 tests
"""
from unittest import mock
import phonenumbers
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError
from .serializers import VerifyVerificationCodeSerializer

PHONE_NUMBER = "+55 11 98070-6050"
CODE = "1234"

class VerifyVerificationCodeSerializerTestCase(TestCase):
    """
    VerifyVerificationCodeSerializer test case
    """
    @mock.patch("rollsocialnetwork.api.v1.serializers.authenticate")
    def test_validate_ok(self, authenticate_mock):
        """
        .validate ok
        """
        user_model = get_user_model()
        user = user_model()
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
