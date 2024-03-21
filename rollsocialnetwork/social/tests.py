"""
social tests
"""
from unittest import mock
from django.test import (
    RequestFactory,
    TestCase
)
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.core.exceptions import BadRequest
from django.http import HttpResponseRedirect, JsonResponse
from rollsocialnetwork.tests_factory import UserFactory
from .context_processors import social
from .mixins import UserProfileRequiredMixin
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

class TestBaseView(View):
    """
    Teste Base View
    """

class UPRMTestView(UserProfileRequiredMixin,
                   TestBaseView):
    """
    UPRM Test View

    extends UserProfileRequiredMixin and TestBaseView
    """

class UserProfileRequiredMixinTest(TestCase):
    """
    UserProfileRequiredMixin test
    """

    def setUp(self):
        self.server_name = "roll.local"
        self.factory = RequestFactory(SERVER_NAME=self.server_name)
        user_factory = UserFactory()
        user_profile_factory = UserProfileFactory()
        self.user = user_factory.create_user()
        self.user_profile = user_profile_factory.create_user_profile(user=self.user)

    def test_is_action_component_true(self):
        """
        test is_action_component property, true when request has Action-Component header
        """
        request = self.factory.get("/test/", headers={"Action-Component": "example"})
        is_action_component = UPRMTestView(request=request).is_action_component
        self.assertTrue(is_action_component)

    def test_is_action_component_false(self):
        """
        test is_action_component property, false when request hasn't Action-Component header
        """
        request = self.factory.get("/test/")
        is_action_component = UPRMTestView(request=request).is_action_component
        self.assertFalse(is_action_component)

    def test_get_login_url_not_authenticated(self):
        """
        test get_login_url method, returns LOGIN_URL when user is not authenticated
        """
        request = self.factory.get("/test/")
        request.user = AnonymousUser()
        login_url = UPRMTestView(request=request).get_login_url()
        self.assertEqual(login_url, settings.LOGIN_URL)

    def test_get_login_url_authenticated_without_user_profile(self):
        """
        test get_login_url method, returns CREATE_USER_PROFILE_URL when user is authenticated but
        request not has user profile
        """
        request = self.factory.get("/test/")
        request.user = self.user
        login_url = UPRMTestView(request=request).get_login_url()
        self.assertEqual(login_url, settings.CREATE_USER_PROFILE_URL)

    def test_get_login_url_authenticated_with_user_profile(self):
        """
        test get_login_url method, raise BadRequest when user is authenticated and request has user
        profile
        """
        request = self.factory.get("/test/")
        request.user = self.user
        request.user_profile = self.user_profile
        with self.assertRaises(BadRequest):
            UPRMTestView(request=request).get_login_url()

    def test_get_permission_denied_message_not_authenticated(self):
        """
        test get_permission_denied_message method, returns message when user is not authenticated
        """
        request = self.factory.get("/test/")
        request.user = AnonymousUser()
        permission_denied_message = UPRMTestView(request=request).get_permission_denied_message()
        self.assertEqual(permission_denied_message, "You are not authenticated.")

    def test_get_permission_denied_message_authenticated_without_user_profile(self):
        """
        test get_permission_denied_message method, returns message when user is authenticated but
        request not has user profile
        """
        request = self.factory.get("/test/")
        request.user = self.user
        permission_denied_message = UPRMTestView(request=request).get_permission_denied_message()
        self.assertEqual(permission_denied_message, "You do not have a user profile on this roll.")

    def test_get_permission_denied_message_authenticated_with_user_profile(self):
        """
        test get_permission_denied_message method, raise BadRequest when user is authenticated and
        request has user profile
        """
        request = self.factory.get("/test/")
        request.user = self.user
        request.user_profile = self.user_profile
        with self.assertRaises(BadRequest):
            UPRMTestView(request=request).get_permission_denied_message()

    def test_get_action_message_not_authenticated(self):
        """
        test get_action_message method, returns message when user is not authenticated
        """
        request = self.factory.get("/test/")
        request.user = AnonymousUser()
        action_message = UPRMTestView(request=request).get_action_message()
        self.assertEqual(action_message, "Authenticate")

    def test_get_action_message_authenticated_without_user_profile(self):
        """
        test get_action_message method, returns message when user is authenticated but request not
        has user profile
        """
        request = self.factory.get("/test/")
        request.user = self.user
        action_message = UPRMTestView(request=request).get_action_message()
        self.assertEqual(action_message, "Create a profile")

    def test_get_action_message_authenticated_with_user_profile(self):
        """
        test get_action_message method, raise BadRequest when user is authenticated and request has
        user profile
        """
        request = self.factory.get("/test/")
        request.user = self.user
        request.user_profile = self.user_profile
        with self.assertRaises(BadRequest):
            UPRMTestView(request=request).get_action_message()

    @mock.patch.object(UserProfileRequiredMixin, "get_login_url")
    @mock.patch.object(UserProfileRequiredMixin,
                       "is_action_component",
                       new_callable=mock.PropertyMock,
                       return_value=False)
    def test_get_action_url_not_is_action_component(self,
                                                    _is_action_component_mock,
                                                    get_login_url_mock):
        """
        test get_action_url method, not is action component return resolved_url
        """
        route_name = "home"
        get_login_url_mock.return_value = route_name
        request = self.factory.get("/test/")
        action_url = UPRMTestView(request=request).get_action_url()
        self.assertEqual(action_url, reverse(route_name))

    @mock.patch.object(UserProfileRequiredMixin, "get_login_url")
    @mock.patch.object(UserProfileRequiredMixin,
                       "is_action_component",
                       new_callable=mock.PropertyMock,
                       return_value=True)
    def test_get_action_url_is_action_component(self,
                                                _is_action_component_mock,
                                                get_login_url_mock):
        """
        test get_action_url method, is action component return absolute resolved_url
        """
        route_name = "home"
        get_login_url_mock.return_value = route_name
        request = self.factory.get("/test/")
        action_url = UPRMTestView(request=request).get_action_url()
        self.assertEqual(action_url, f"http://{self.server_name}{reverse(route_name)}")

    @mock.patch.object(UserProfileRequiredMixin, "get_login_url")
    @mock.patch.object(UserProfileRequiredMixin,
                       "is_action_component",
                       new_callable=mock.PropertyMock,
                       return_value=True)
    def test_get_action_url_is_action_component_resolved(self,
                                                         _is_action_component_mock,
                                                         get_login_url_mock):
        """
        test get_action_url method, when is action component and get_login_url return a absolute url
        return resolved_url
        """
        absolute_url = "http://example.com/"
        get_login_url_mock.return_value = absolute_url
        request = self.factory.get("/test/")
        action_url = UPRMTestView(request=request).get_action_url()
        self.assertEqual(action_url, absolute_url)

    @mock.patch.object(UserProfileRequiredMixin, "handle_no_permission")
    def test_dispatch_not_authenticated_not_user_profile(self, handle_no_permission_mock):
        """
        test dispatch method, when not authenticated and request hasn't user profile calls
        handle_no_permission method
        """
        request = self.factory.get("/test/")
        request.user = AnonymousUser()
        UPRMTestView(request=request).dispatch(request)
        handle_no_permission_mock.assert_called()

    @mock.patch.object(UserProfileRequiredMixin, "get_action_url")
    @mock.patch.object(UserProfileRequiredMixin,
                       "is_action_component",
                       new_callable=mock.PropertyMock,
                       return_value=False)
    def test_handle_no_permission_not_is_action_component(self,
                                                          _is_action_component_mock,
                                                          get_action_url_mock):
        """
        test handle_no_permission method, returns redirect to login with next
        """
        action_url = "/login/"
        request_path = "/test/"
        get_action_url_mock.return_value = action_url
        request = self.factory.get(request_path)
        response = UPRMTestView(request=request).handle_no_permission()
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, f"{action_url}?next={request_path}")

    @mock.patch.object(UserProfileRequiredMixin,
                       "get_action_message",
                       return_value="do")
    @mock.patch.object(UserProfileRequiredMixin,
                       "get_permission_denied_message",
                       return_value="denied")
    @mock.patch.object(UserProfileRequiredMixin, "get_action_url")
    @mock.patch.object(UserProfileRequiredMixin,
                       "is_action_component",
                       new_callable=mock.PropertyMock,
                       return_value=True)
    def test_handle_no_permission_is_action_component(self,
                                                      _is_action_component_mock,
                                                      get_action_url_mock,
                                                      _get_permission_denied_message_mock,
                                                      _get_action_message_mock):
        """
        test handle_no_permission method, returns json response with correct content
        """
        action_url = "/login/"
        request_path = "/test/"
        get_action_url_mock.return_value = action_url
        request = self.factory.get(request_path)
        response = UPRMTestView(request=request).handle_no_permission()
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(
            response.content,
            b"""{"message": "denied", "action_message": "do", "action_url": "/login/", \
"action_component": "popup-opener-callback", "next": "/test/"}"""
        )
