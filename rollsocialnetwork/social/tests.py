"""
social tests
"""
from django.test import (
    RequestFactory,
    TestCase
)
from .context_processors import social
from .tests_factory import UserProfileFactory

class SocialContextProcessorTest(TestCase):
    """
    social context processor test
    """

    def setUp(self):
        self.factory = RequestFactory()
        user_profile_factory = UserProfileFactory()
        self.user_profile = user_profile_factory.create_user_profile()

    def test_has_user_profile(self):
        """
        test has user profile
        """
        request = self.factory.get("/test/")
        result = social(request)
        self.assertIn("user_profile", result.keys())

    def test_with_user_profile(self):
        """
        test with user profile
        """
        request = self.factory.get("/test/")
        request.user_profile = self.user_profile
        result = social(request)
        result_user_profile = result.get("user_profile")
        self.assertEqual(result_user_profile.id, self.user_profile.id)
