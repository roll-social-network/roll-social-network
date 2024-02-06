"""
timeline posts templatetags

usage:

{% load posts %}
"""
from django import template

from rollsocialnetwork.timeline.models import Post
from rollsocialnetwork.social.models import UserProfile

register = template.Library()

def has_like(post: Post, user_profile: UserProfile):
    """
    has like
    """
    return post.get_like(user_profile) is not None

register.filter("has_like", has_like)
