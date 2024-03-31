"""
phone auth tests
"""
from datetime import timedelta
from unittest import mock
from django.test import (
    RequestFactory,
    TestCase,
    override_settings
)
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.forms import ValidationError
from rollsocialnetwork.tests_factory import SiteFactory, UserFactory
from rollsocialnetwork.tests_fake import fake
from .utils import (
    get_or_create_user,
    normalize_phone_number,
)
from .models import (
    VerificationCode,
    OTPSecret,
)
from . import forms
from .tests_factory import (
    VerificationCodeFactory,
    OTPSecretFactory,
)

PHONE_1 = "+55 11 98070-6050"
PHONE_2 = "+55 11 98070-6051"

disable_phone_auth_sms_gateway = override_settings(PHONE_AUTH_SMS_GATEWAY="disabled")

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
    @disable_phone_auth_sms_gateway
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
    @disable_phone_auth_sms_gateway
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

class PhoneAuthBackendTestCase(TestCase):
    """
    phone auth backend test case
    """
    def setUp(self):
        self.factory = RequestFactory()
        user_factory = UserFactory()
        self.verification_code_factory = VerificationCodeFactory()
        self.user = user_factory.create_user()

    def test_authenticate_with_correct_phone_number_and_code(self):
        """
        test authenticate with correct phone number and code
        """
        verification_code = self.verification_code_factory.create_verification_code(user=self.user)
        response = self.client.login(request=self.factory.post("/login/"),
                                     phone_number=self.user.username,
                                     code=verification_code.code)
        self.assertTrue(response)

    def test_authenticate_incorrect(self):
        """
        test authenticate incorrect
        """
        response = self.client.login(phone_number=self.user.username,
                                     code="1234")
        self.assertFalse(response)

class VerifyVerificationCodeFormTestCase(TestCase):
    """
    verify verification code form test case
    """
    def setUp(self):
        self.user_factory = UserFactory()

    @mock.patch.object(forms, "authenticate")
    def test_valid_login(self, authenticate_mock):
        """
        test valid login
        """
        user = self.user_factory.create_user()
        authenticate_mock.return_value = user
        form = forms.VerifyVerificationCodeForm(data={"phone": user.username, "code": "1234"})
        is_valid = form.is_valid()
        self.assertTrue(is_valid)
        cleaned_data = form.clean()
        self.assertIsInstance(cleaned_data, dict)

    @mock.patch.object(forms, "authenticate")
    def test_invalid_login(self, authenticate_mock):
        """
        test invalid login
        """
        authenticate_mock.return_value = None
        form = forms.VerifyVerificationCodeForm(data={"phone": fake.e164(), "code": "1234"})
        is_valid = form.is_valid()
        self.assertFalse(is_valid)
        with self.assertRaises(ValidationError):
            form.clean()

class OTPSecretVerifyTestCase(TestCase):
    """
    tests for OTPSecret.verify() class method
    """

    def setUp(self) -> None:
        otp_secret_factory = OTPSecretFactory()
        self.otp_secret = otp_secret_factory.create_otp_secret()

    def test_verify_ok(self):
        """
        test verify ok
        """
        result = OTPSecret.verify(self.otp_secret.user.username,
                                  self.otp_secret.totp.now())
        self.assertIsNotNone(result)
        self.assertIsInstance(result, OTPSecret)

    def test_verify_wrong_code(self):
        """
        test verify wrong code
        """
        result = OTPSecret.verify(self.otp_secret.user.username,
                                  "000000")
        self.assertIsNone(result)

    def test_verify_user_not_exists(self):
        """
        test verify user not exists
        """
        result = OTPSecret.verify("+00000000",
                                  "000000")
        self.assertIsNone(result)

class OTPSecretPhoneNumberHasOTPSecretTestCase(TestCase):
    """
    tests for OTPSecret.phone_number_has_otp_secret() class method
    """

    def setUp(self) -> None:
        otp_secret_factory = OTPSecretFactory()
        self.otp_secret = otp_secret_factory.create_otp_secret()

    def test_exist(self):
        """
        test exist
        """
        result = OTPSecret.phone_number_has_otp_secret(self.otp_secret.user.username)
        self.assertTrue(result)

    def test_not_exist(self):
        """
        test not exist
        """
        result = OTPSecret.phone_number_has_otp_secret("+00000000")
        self.assertFalse(result)

class OTPSecretURITestCase(TestCase):
    """
    tests for OTPSecret.uri class property
    """

    def setUp(self) -> None:
        otp_secret_factory = OTPSecretFactory()
        site_factory = SiteFactory()
        self.site = site_factory.create_site()
        self.otp_secret = otp_secret_factory.create_otp_secret()

    def test_has_home_site_info(self):
        """
        test has home site info
        """
        with override_settings(HOME_SITE_ID=self.site.id):
            result = self.otp_secret.uri
            self.assertIn(self.site.name, result)
