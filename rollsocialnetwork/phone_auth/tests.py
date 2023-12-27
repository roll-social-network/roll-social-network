"""
phone auth tests
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from .utils import (
    get_or_create_user,
    normalize_phone_number,
)
from .models import VerificationCode

PHONE_1 = "+55 11 98070-6050"
PHONE_2 = "+55 11 98070-6051"

class GetOrCreateUserTestCase(TestCase):
    """
    tests for get_or_create_user() function
    """
    def setUp(self):
        user_model = get_user_model()
        pn = normalize_phone_number(PHONE_1)
        self.user_1 = user_model(**{user_model.USERNAME_FIELD: pn})
        self.user_1.save()

    def test_get_ok(self):
        """
        get ok
        """
        user = get_or_create_user(PHONE_1)
        self.assertEqual(user.pk, self.user_1.pk)

    def test_create_ok(self):
        """
        create ok
        """
        user = get_or_create_user(PHONE_2)
        self.assertIsNotNone(user.pk)

class VerificationCodeRequestTestCase(TestCase):
    """
    tests for VerificationCode.request() class method
    """
    def test_request_ok(self):
        """
        request ok
        """
        verification_code = VerificationCode.request(PHONE_1)
        self.assertIsNotNone(verification_code.pk)

class VerificationCodeVerifyTestCase(TestCase):
    """
    tests for VerificationCode.verify() class method
    """
    def setUp(self):
        verification_code = VerificationCode.request(PHONE_1)
        self.code = verification_code.code

    def test_verify_ok(self):
        """
        verify ok
        """
        verification_code = VerificationCode.verify(PHONE_1, self.code)
        self.assertIsNotNone(verification_code)
        self.assertIsInstance(verification_code, VerificationCode)

    def test_verify_wrong_phone_number(self):
        """
        verify with wrong phone number
        """
        verification_code = VerificationCode.verify(PHONE_2, self.code)
        self.assertIsNone(verification_code)

    def test_verify_wrong_code(self):
        """
        verify with wrong code
        """
        verification_code = VerificationCode.verify(PHONE_1, "0000")
        self.assertIsNone(verification_code)
