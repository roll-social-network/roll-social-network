from django.test import TestCase
from django.contrib.auth import get_user_model
from .utils import (
    get_or_create_user,
    normalize_phone_number,
)
from rollsocialnetwork.phone_auth.models import VerificationCode

PHONE_1 = "+55 11 98070-6050"
PHONE_2 = "+55 11 98070-6051"

class GetOrCreateUserTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        pn = normalize_phone_number(PHONE_1)
        self.user_1 = User(**{User.USERNAME_FIELD: pn})
        self.user_1.save()

    def test_get_ok(self):
        user = get_or_create_user(PHONE_1)
        self.assertEqual(user.pk, self.user_1.pk)

    def test_create_ok(self):
        user = get_or_create_user(PHONE_2)
        self.assertIsNotNone(user.pk)

class VerificationCodeRequestTestCase(TestCase):
    def test_request_ok(self):
        verification_code = VerificationCode.request(PHONE_1)
        self.assertIsNotNone(verification_code.pk)
