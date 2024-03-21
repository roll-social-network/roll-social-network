"""
rollsocialnetwork tests
"""
from django.test import (
    TestCase,
    RequestFactory,
    override_settings
)
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseRedirect
)
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlencode
from .views import NginxAccelRedirectView
from .tests_factory import (
    SiteFactory,
    UserFactory,
)
from .opener_callback import OpenerCallbackRedirectURLMixin
from .context_processors import is_home_site

class LogoutViewTest(TestCase):
    """
    LogoutView test
    """

    def setUp(self):
        site_factory = SiteFactory()
        self.site = site_factory.create_site()

    def test_get(self):
        """
        test get
        """
        response = self.client.get(
            reverse("logout"),
            SERVER_NAME=self.site.domain
        )
        self.assertIsInstance(response, HttpResponseRedirect)

class NginxAccelRedirectViewTest(TestCase):
    """
    NginxAccelRedirectView test
    """
    def setUp(self):
        self.factory = RequestFactory()
        site_factory = SiteFactory()
        user_factory = UserFactory()
        self.site = site_factory.create_site()
        self.user = user_factory.create_user()

    def test_not_authenticated(self):
        """
        test not authenticated
        """
        path = "file.jpg"
        request = self.factory.get(
            f"/media/{path}",
            SERVER_NAME=self.site.domain
        )
        request.user = AnonymousUser()
        response = NginxAccelRedirectView.as_view()(request, path=path)
        self.assertIsInstance(response, HttpResponseForbidden)

    def test_authenticated(self):
        """
        test authenticated
        """
        path = "file.jpg"
        request = self.factory.get(
            f"/media/{path}",
            SERVER_NAME=self.site.domain
        )
        request.user = self.user
        response = NginxAccelRedirectView.as_view()(request, path=path)
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["X-Accel-Redirect"],
            f"{settings.NGINX_ACCEL_REDIRECT_INTERNAL_LOCATION}{path}"
        )

class TestBaseView:  # pylint: disable=R0903
    """
    Test Base View
    """

    DEFAULT_REDIRECT_URL = "default/url"

    def __init__(self, request):
        self.request = request

    def get_redirect_url(self):
        """
        get redirect url
        """
        return TestBaseView.DEFAULT_REDIRECT_URL

class OCTestView(OpenerCallbackRedirectURLMixin,  # pylint: disable=R0903
                 TestBaseView):
    """
    OC Test View

    extends OpenerCallbackRedirectURLMixin and OCTestBaseView
    """

class OpenerCallbackRedirectURLMixinTest(TestCase):
    """
    OpenerCallbackRedirectURLMixin test
    """

    def setUp(self):
        self.factory = RequestFactory()

    def test_not_message(self):
        """
        test not message
        """
        request = self.factory.get("/octest/")
        oc_test = OCTestView(request)
        redirect_url = oc_test.get_redirect_url()
        self.assertEqual(redirect_url, TestBaseView.DEFAULT_REDIRECT_URL)

    def test_with_message(self):
        """
        test with message
        """
        message_field = OpenerCallbackRedirectURLMixin.MESSAGE_FIELD_NAME
        message = "message"
        opener_callback_url = reverse("opener_callback")
        request = self.factory.get(f"/octest/?{message_field}={message}")
        oc_test = OCTestView(request)
        redirect_url = oc_test.get_redirect_url()
        qs = {
            "message": message
        }
        self.assertEqual(redirect_url, f"{opener_callback_url}?{urlencode(qs)}")

    def test_with_message_and_origin(self):
        """
        test with message and origin
        """
        message_field = OpenerCallbackRedirectURLMixin.MESSAGE_FIELD_NAME
        origin_field = OpenerCallbackRedirectURLMixin.ORIGIN_FIELD_NAME
        message = "message"
        origin = "http://example.com"
        opener_callback_url = reverse("opener_callback")
        request = self.factory.get(f"/octest/?{message_field}={message}&{origin_field}={origin}")
        oc_test = OCTestView(request)
        redirect_url = oc_test.get_redirect_url()
        qs = {
            "message": message,
            "origin": origin
        }
        self.assertEqual(redirect_url, f"{opener_callback_url}?{urlencode(qs)}")

class IsHomeSiteContextProcessorTest(TestCase):
    """
    is_home_site context processor test
    """

    def setUp(self):
        self.factory = RequestFactory()
        site_factory = SiteFactory()
        self.site = site_factory.create_site()

    def test_is(self):
        """
        is home site
        """
        request = self.factory.get(
            "/test/",
            SERVER_NAME=self.site.domain
        )
        request.site = self.site
        with override_settings(HOME_SITE_ID=self.site.id):
            result = is_home_site(request)
            result_is_home_site = result.get("is_home_site")
            self.assertTrue(result_is_home_site)

    def test_not_is(self):
        """
        not is home site
        """
        request = self.factory.get(
            "/test/",
            SERVER_NAME=self.site.domain
        )
        request.site = self.site
        with override_settings(HOME_SITE_ID=0):
            result = is_home_site(request)
            result_is_home_site = result.get("is_home_site")
            self.assertFalse(result_is_home_site)
