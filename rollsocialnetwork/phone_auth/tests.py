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
from rollsocialnetwork.phone_auth.views import LoginView, ValidateOTPSecretView
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
from .forms import (
    VerifyVerificationCodeForm,
    VerifyOTPCodeForm,
)
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

    @mock.patch.object(VerifyVerificationCodeForm,
                       "authenticate_fn")
    def test_valid_login(self, authenticate_mock):
        """
        test valid login
        """
        user = self.user_factory.create_user()
        authenticate_mock.return_value = user
        form = VerifyVerificationCodeForm(data={"phone_number": user.username, "code": "1234"})
        is_valid = form.is_valid()
        self.assertTrue(is_valid)
        cleaned_data = form.clean()
        self.assertIsInstance(cleaned_data, dict)

    @mock.patch.object(VerifyVerificationCodeForm,
                       "authenticate_fn")
    def test_invalid_login(self, authenticate_mock):
        """
        test invalid login
        """
        authenticate_mock.return_value = None
        form = VerifyVerificationCodeForm(data={"phone_number": fake.e164(), "code": "1234"})
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
    tests for OTPSecret.phone_number_has_valid_otp_secret() class method
    """

    def setUp(self) -> None:
        otp_secret_factory = OTPSecretFactory()
        self.otp_secret = otp_secret_factory.create_otp_secret()
        self.otp_secret.validate()
        self.otp_secret_not_valid = otp_secret_factory.create_otp_secret()

    def test_exist_valid(self):
        """
        test exist
        """
        result = OTPSecret.phone_number_has_valid_otp_secret(self.otp_secret.user.username)
        self.assertTrue(result)

    def test_not_exist(self):
        """
        test not exist
        """
        result = OTPSecret.phone_number_has_valid_otp_secret("+00000000")
        self.assertFalse(result)

    def test_exists_but_not_valid(self):
        """
        test exists but not valid
        """
        result = OTPSecret.phone_number_has_valid_otp_secret(
            self.otp_secret_not_valid.user.username)
        self.assertFalse(result)

class OTPSecretURITestCase(TestCase):
    """
    tests for OTPSecret.uri class property
    """

    def setUp(self) -> None:
        otp_secret_factory = OTPSecretFactory()
        site_factory = SiteFactory()
        self.site = site_factory.create_site(name="cats-site")
        self.otp_secret = otp_secret_factory.create_otp_secret()

    def test_has_home_site_info(self):
        """
        test has home site info
        """
        with override_settings(HOME_SITE_ID=self.site.id):
            result = self.otp_secret.uri
            self.assertIn(self.site.name, result)

class PhoneAuthOTPBackendTestCase(TestCase):
    """
    phone auth OTP backend test case
    """
    def setUp(self):
        self.factory = RequestFactory()
        user_factory = UserFactory()
        self.otp_secret_factory = OTPSecretFactory()
        self.user = user_factory.create_user()

    def test_authenticate_with_correct_phone_number_and_otp_code(self):
        """
        test authenticate with correct phone number and otp code
        """
        otp_secret = self.otp_secret_factory.create_otp_secret(user=self.user)
        response = self.client.login(request=self.factory.post("/login/"),
                                     phone_number=self.user.username,
                                     otp_code=otp_secret.totp.now())
        self.assertTrue(response)

    def test_authenticate_incorrect(self):
        """
        test authenticate incorrect
        """
        response = self.client.login(phone_number=self.user.username,
                                     otp_code="1234")
        self.assertFalse(response)

class VerifyOTPCodeFormAuthenticateTestCase(TestCase):
    """
    tests for VerifyOTPCodeForm.call_authenticate() method
    """

    def setUp(self):
        user_factory = UserFactory()
        self.user = user_factory.create_user()

    @mock.patch.object(VerifyOTPCodeForm,
                       "authenticate_fn")
    def test_called_with_correct_kwargs(self, authenticate_mock):
        """
        test called with correct kwargs
        """
        authenticate_mock.returns_value = self.user
        form = VerifyOTPCodeForm()
        pn = "+0000000"
        code = "0000"
        form.call_authenticate(pn, code)
        authenticate_mock.assert_called_with(phone_number=pn, otp_code=code)

class LoginViewGetVerifyURLTestCase(TestCase):
    """
    tests for LoginView.get_verify_url() method
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.phone_number = fake.e164()

    @mock.patch.object(OTPSecret, "phone_number_has_valid_otp_secret", return_value=True)
    def test_has_valid_otp_secret(self, _phone_number_has_valid_otp_secret_mock):
        """
        test has valid OTP Secret
        """
        request = self.factory.post("/login/", {"phone_number": self.phone_number})
        view = LoginView(request=request)
        form = view.get_form()
        is_valid = form.is_valid()
        self.assertTrue(is_valid)
        result = view.get_verify_url(form)
        self.assertEqual(result, f"/phone-auth/verify-otp/{self.phone_number}/")

    @mock.patch.object(OTPSecret, "phone_number_has_valid_otp_secret", return_value=False)
    def test_hasnt_valid_otp_secret(self, _phone_number_has_valid_otp_secret_mock):
        """
        test hasn't valid OTP secret
        """
        request = self.factory.post("/login/", {"phone_number": self.phone_number})
        view = LoginView(request=request)
        form = view.get_form()
        is_valid = form.is_valid()
        self.assertTrue(is_valid)
        result = view.get_verify_url(form)
        self.assertEqual(result, f"/phone-auth/request/{self.phone_number}/")

class ValidateOTPSecretViewTestCase(TestCase):
    """
    tests for ValidateOTPSecretView
    """

    def setUp(self):
        self.factory = RequestFactory()
        otp_secret_factory = OTPSecretFactory()
        self.otp_secret = otp_secret_factory.create_otp_secret()
        self.otp_secret_valid = otp_secret_factory.create_otp_secret(valid_at=timezone.now())

    def test_get_not_valid(self):
        """
        test get not valid OTP secret
        """
        request = self.factory.get("/validate/")
        request.user = self.otp_secret.user
        result = ValidateOTPSecretView.as_view()(request)
        self.assertEqual(result.status_code, 200)

    def test_get_valid(self):
        """
        test get valid OTP secret
        """
        request = self.factory.get("/validate/")
        request.user = self.otp_secret_valid.user
        result = ValidateOTPSecretView.as_view()(request)
        self.assertEqual(result.status_code, 400)

    @mock.patch.object(OTPSecret, "validate")
    def test_validate(self, validate_mock):
        """
        test validate post with valid code
        """
        request = self.factory.post("/validate/", { "code": self.otp_secret.totp.now() })
        request.user = self.otp_secret.user
        result = ValidateOTPSecretView.as_view()(request)
        self.assertEqual(result.status_code, 302)
        validate_mock.assert_called()
