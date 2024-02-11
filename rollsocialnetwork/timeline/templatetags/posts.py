"""
timeline posts templatetags

usage:

{% load posts %}
"""
from django import template
from django.contrib.sites.models import Site
from rollsocialnetwork.timeline.models import Post
from rollsocialnetwork.social.models import UserProfile

register = template.Library()

def has_like(post: Post, user_profile: UserProfile):
    """
    has like
    """
    return post.get_like(user_profile) is not None

def is_external_post(post: Post, site: Site):
    """
    is external post
    """
    return post.user_profile.site.pk != site.pk

register.filter("has_like", has_like)
register.filter("is_external_post", is_external_post)
