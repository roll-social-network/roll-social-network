"""
oidc tests
"""
from django.test import TestCase
from social_core.exceptions import AuthException  # type: ignore[import-untyped]
from rollsocialnetwork.tests_factory import UserFactory
from .backends import RollOpenIdConnectAuth
from .pipeline import associate_roll_user

class TestAssociateRollUser(TestCase):
    """
    associate_roll_user pipe test case
    """
    def setUp(self):
        self.backend = RollOpenIdConnectAuth()

    def test_without_username(self):
        """
        test without username
        """
        details = {}
        result = associate_roll_user(self.backend,
                                     details,
                                     user=None)
        self.assertIsNone(result)

    def test_with_user_setted(self):
        """
        test with user setted
        """
        user_factory = UserFactory()
        user = user_factory.create_user()
        details = {
            "username": user.get_username()
        }
        result = associate_roll_user(self.backend,
                                     details,
                                     user=user)
        self.assertIsNone(result)

    def test_user_not_exists(self):
        """
        test user not exists
        """
        details = {
            "username": "user"
        }
        with self.assertRaises(AuthException):
            associate_roll_user(self.backend,
                                details,
                                user=None)

    def test_return_user(self):
        """
        test return user
        """
        user_factory = UserFactory()
        user = user_factory.create_user()
        details = {
            "username": user.get_username()
        }
        result = associate_roll_user(self.backend,
                                     details,
                                     user=None)
        self.assertDictEqual(result, { "user": user, "is_new": False })
