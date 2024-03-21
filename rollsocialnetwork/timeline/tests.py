"""
timeline tests
"""
from unittest import mock
from django.test import TestCase
from django.http import HttpResponseRedirect
from rollsocialnetwork.social.tests_factory import UserProfileFactory
from rollsocialnetwork.tests_factory import SiteFactory
from rollsocialnetwork.timeline.models import Like, Post
from .mixins import TimelineViewMixin
from .tests_factory import PostFactory

class TimelineViewMixinTest(TestCase):
    """
    timeline view test
    """
    def setUp(self):
        self.post_factory = PostFactory()

    def _get_queryset(self):
        return []

    @mock.patch.object(TimelineViewMixin, 'get_slice_value', return_value=None)
    def test_fill_slice_value_empty_posts(self, _get_slice_value_mock):
        """
        test fill slice value returns None
        """
        mixin = TimelineViewMixin()
        mixin.get_queryset = mock.MagicMock()
        mixin.get_queryset.return_value = Post.objects.all()
        self.assertIsNone(mixin.fill_slice_value())

    @mock.patch.object(TimelineViewMixin, 'get_slice_value', return_value=None)
    def test_fill_slice_value_older_post(self, _get_slice_value_mock):
        """
        test fill slice value is older post pk
        """
        _post_1 = self.post_factory.create_post()
        post_2 = self.post_factory.create_post()
        mixin = TimelineViewMixin()
        mixin.get_queryset = mock.MagicMock()
        mixin.get_queryset.return_value = Post.objects.all()
        self.assertEqual(mixin.fill_slice_value(), str(post_2.pk))

    @mock.patch.object(TimelineViewMixin, 'get_slice_value')
    def test_fill_has_new_post_out_slice_comportament(self, get_slice_value_mock):
        """
        test fill has new post out slice comportament
        """
        post_1 = self.post_factory.create_post()
        get_slice_value_mock.return_value = post_1.pk
        mixin = TimelineViewMixin()
        self.assertFalse(mixin.fill_has_new_post_out_slice())
        _post_2 = self.post_factory.create_post()
        self.assertTrue(mixin.fill_has_new_post_out_slice())

    @mock.patch.object(TimelineViewMixin, 'fill_slice_value', return_value=None)
    @mock.patch.object(TimelineViewMixin, 'fill_has_new_post_out_slice', return_value=None)
    def test_build_context_data_comportament(self,
                                             _fill_has_new_post_out_slice_mock,
                                             _fill_slice_value_mock):
        """
        test get context data comportament
        """
        mixin = TimelineViewMixin()
        context_data = mixin.build_context_data()
        self.assertIn("slice_kwarg", context_data.keys())
        self.assertIn("slice", context_data.keys())
        self.assertIn("has_new_post_out_slice", context_data.keys())

class PostLikeDislikeTest(TestCase):
    """
    post like dislike test
    """
    def setUp(self):
        self.user_profile_factory = UserProfileFactory()
        self.post_factory = PostFactory()
        self.user_profile = self.user_profile_factory.create_user_profile()

    def test_get_like_returns(self):
        """
        test get like returns
        """
        post = self.post_factory.create_post()
        self.assertIsNone(post.get_like(self.user_profile))
        post._like(self.user_profile)  # pylint: disable=protected-access
        self.assertIsInstance(post.get_like(self.user_profile), Like)

    def test_like_dislike_comportament(self):
        """
        test like dislike comportament
        """
        post = self.post_factory.create_post()
        like = post.like_dislike(self.user_profile)
        self.assertIsInstance(like, Like)
        self.assertEqual(like.user_profile, self.user_profile)
        self.assertEqual(like.post, post)
        self.assertIsNone(post.like_dislike(self.user_profile))

class PostLikeDislikeViewTest(TestCase):
    """
    post like dislike view test
    """
    def setUp(self):
        user_profile_factory = UserProfileFactory()
        site_factory = SiteFactory()
        post_factory = PostFactory()
        self.site = site_factory.create_site()
        self.user_profile = user_profile_factory.create_user_profile(site=self.site)
        self.post = post_factory.create_post(user_profile=self.user_profile)
        self.client.force_login(self.user_profile.user)

    def test_like_dislike_view_comportament(self):
        """
        test like dislike view comportament
        """
        response = self.client.get(
            f"/t/post/{self.post.pk}/like-dislike/",
            SERVER_NAME=self.site.domain,
        )
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, f"/t/#post-{self.post.pk}")
        like = self.post.get_like(self.user_profile)
        self.assertIsNotNone(like)
        self.assertEqual(like.user_profile, self.user_profile)
        response = self.client.get(
            f"/t/post/{self.post.pk}/like-dislike/",
            SERVER_NAME=self.site.domain,
        )
        like = self.post.get_like(self.user_profile)
        self.assertIsNone(like)

    def test_like_dislike_action_component_comportament(self):
        """
        test like dislike action component comportament
        """
        response = self.client.get(
            f"/t/post/{self.post.pk}/like-dislike/",
            SERVER_NAME=self.site.domain,
            headers={
                "Action-Component": "like-dislike",
            }
        )
        self.assertEqual(response.status_code, 201)
        like = self.post.get_like(self.user_profile)
        self.assertIsNotNone(like)
        self.assertEqual(like.user_profile, self.user_profile)
        response = self.client.get(
            f"/t/post/{self.post.pk}/like-dislike/",
            SERVER_NAME=self.site.domain,
            headers={
                "Action-Component": "like-dislike",
            }
        )
        self.assertEqual(response.status_code, 204)
        like = self.post.get_like(self.user_profile)
        self.assertIsNone(like)
