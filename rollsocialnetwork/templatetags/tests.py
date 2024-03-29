"""
templatetags tests
"""
from django.test import (
    TestCase,
    RequestFactory,
    override_settings
)
from django.template import Context
from rollsocialnetwork.tests_factory import SiteFactory
from .uris import site_build_absolute_uri

class SiteBuildAbsoluteURITemplateTagTest(TestCase):
    """
    site_build_absolute_uri template tag test
    """

    def setUp(self):
        self.factory = RequestFactory()
        site_factory = SiteFactory()
        self.site = site_factory.create_site()
        self.other_site = site_factory.create_site()

    def test_is_current_site(self):
        """
        test is current site returns path
        """
        context = Context()
        context.request = self.factory.get("/test/")
        context.request.site = self.site
        result = site_build_absolute_uri(context,
                                         self.site,
                                         "home")
        self.assertEqual(result, "/")

    def test_is_other_site(self):
        """
        test is other site return absolute url
        """
        context = Context()
        context.request = self.factory.get("/test/")
        context.request.site = self.site
        result = site_build_absolute_uri(context,
                                         self.other_site,
                                         "home")
        self.assertEqual(result, f"http://{self.other_site.domain}/")

    def test_is_other_site_with_override_scheme(self):
        """
        test is other site return absolute url with override scheme
        """
        context = Context()
        context.request = self.factory.get("/test/")
        context.request.site = self.site
        with override_settings(OVERRIDE_SCHEME="https"):
            result = site_build_absolute_uri(context,
                                            self.other_site,
                                            "home")
            self.assertEqual(result, f"https://{self.other_site.domain}/")
