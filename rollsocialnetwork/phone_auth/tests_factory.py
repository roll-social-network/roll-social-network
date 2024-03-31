"""
phone auth tests factory
"""
from rollsocialnetwork.tests_factory import UserFactory
from .models import (
    OTPSecret,
    VerificationCode,
)

class VerificationCodeFactory:
    """
    verification code factory
    """
    def __init__(self) -> None:
        self.user_factory = UserFactory()

    def factory_verification_code(self, user=None) -> dict:
        """
        factory verification code
        """
        return {
            "user": user or self.user_factory.create_user(),
        }

    def create_verification_code(self, **kwargs) -> VerificationCode:
        """
        create verification code
        """
        return VerificationCode.objects.create(**self.factory_verification_code(**kwargs))

class OTPSecretFactory:
    """
    OTP secret factory
    """
    def __init__(self) -> None:
        self.user_factory = UserFactory()

    def factory_otp_secret(self, user=None) -> dict:
        """
        factory OTP secret
        """
        return {
            "user": user or self.user_factory.create_user(),
        }

    def create_otp_secret(self, **kwargs) -> OTPSecret:
        """
        create OTP secret
        """
        return OTPSecret.objects.create(**self.factory_otp_secret(**kwargs))
