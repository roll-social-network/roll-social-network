"""
phone auth tests
"""
from datetime import timedelta
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
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
        verification_code_1 = VerificationCode.request(PHONE_1)
        self.code_1 = verification_code_1.code
        verification_code_2 = VerificationCode.request(PHONE_1)
        verification_code_2.valid_until = timezone.now() - timedelta(seconds=1)
        verification_code_2.save()
        self.code_2 = verification_code_2.code
        self.verification_code_3 = VerificationCode.request(PHONE_2)
        self.code_3 = self.verification_code_3.code
        verification_code_4 = VerificationCode.request(PHONE_2)
        verification_code_4.attempts = 0
        verification_code_4.save()
        self.code_4 = verification_code_4.code

    def test_verify_ok(self):
        """
        verify ok
        """
        verification_code = VerificationCode.verify(PHONE_1, self.code_1)
        self.assertIsNotNone(verification_code)
        self.assertIsInstance(verification_code, VerificationCode)

    def test_try_verify_wrong_phone_number(self):
        """
        try verify with wrong phone number
        """
        verification_code = VerificationCode.verify(PHONE_2, self.code_1)
        self.assertIsNone(verification_code)

    def test_try_verify_wrong_code(self):
        """
        try verify with wrong code
        """
        verification_code = VerificationCode.verify(PHONE_1, "0000")
        self.assertIsNone(verification_code)

    def test_try_verify_expired_valid_until(self):
        """
        try verify with expired valid until
        """
        verification_code = VerificationCode.verify(PHONE_1, self.code_2)
        self.assertIsNone(verification_code)

    def test_verify_decreases_attempts(self):
        """
        verify decreases attempts
        """
        initial_attempts = self.verification_code_3.attempts
        VerificationCode.verify(PHONE_2, "0000")
        verification_code = VerificationCode.objects.get(pk=self.verification_code_3.pk)
        self.assertEqual(initial_attempts - verification_code.attempts, 1)

    def test_try_verify_no_more_tries(self):
        """
        try verify no more tries
        """
        verification_code = VerificationCode.verify(PHONE_2, self.code_4)
        self.assertIsNone(verification_code)
