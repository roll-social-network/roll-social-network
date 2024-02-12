"""
phone auth tests factory
"""
from rollsocialnetwork.tests_factory import UserFactory
from .models import VerificationCode

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
