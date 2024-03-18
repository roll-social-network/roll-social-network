"""
timeline posts templatetags

usage:

{% load posts %}
"""
from typing import Type
from django import template
from django.contrib.sites.models import Site
from django.contrib.auth.models import AbstractUser
from rollsocialnetwork.timeline.models import Post

register = template.Library()

def has_user_like(post: Post, user: Type[AbstractUser]) -> bool:
    """
    has like
    """
    return post.has_user_like(user)

def is_external_post(post: Post, site: Site):
    """
    is external post
    """
    return post.user_profile.site.pk != site.pk

register.filter("has_user_like", has_user_like)
register.filter("is_external_post", is_external_post)
