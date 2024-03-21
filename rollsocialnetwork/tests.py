from unittest import mock
from django.test import (
    TestCase,
    RequestFactory
)
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseRedirect
)
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.urls import reverse
from .views import NginxAccelRedirectView
from .tests_factory import (
    SiteFactory,
    UserFactory,
)

class LogoutViewTest(TestCase):
    def setUp(self):
        site_factory = SiteFactory()
        self.site = site_factory.create_site()

    def test_get(self):
        response = self.client.get(
            reverse("logout"),
            SERVER_NAME=self.site.domain
        )
        self.assertIsInstance(response, HttpResponseRedirect)

class NginxAccelRedirectViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        site_factory = SiteFactory()
        user_factory = UserFactory()
        self.site = site_factory.create_site()
        self.user = user_factory.create_user()

    def test_not_authenticated(self):
        path = "file.jpg"
        request = self.factory.get(
            f"/media/{path}",
            SERVER_NAME=self.site.domain
        )
        request.user = AnonymousUser()
        response = NginxAccelRedirectView.as_view()(request, path=path)
        self.assertIsInstance(response, HttpResponseForbidden)

    def test_authenticated(self):
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
