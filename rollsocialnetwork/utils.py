"""
rollsocialnetwork utils
"""

from typing import Optional
from datetime import timedelta
from django.db.models import (
    QuerySet,
    Count,
    Q
)
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils import timezone


def get_popular_rolls(qs: Optional[QuerySet[Site]] = None) -> QuerySet[Site]:
    """
    get popular sites
    """
    if not qs:
        qs = Site.objects.exclude(id=settings.HOME_SITE_ID)
    hot_posts_slice = timezone.now() - timedelta(hours=settings.HOT_POSTS_SLICE)
    hot_posts_slice_filter = Q(profiles__posts__created_at__gte=hot_posts_slice)
    return qs.annotate(profiles_count=Count("profiles"),
                       posts_count=Count("profiles__posts"),
                       hot_posts_count=Count("profiles__posts",
                                             filter=hot_posts_slice_filter))\
                        .order_by("-hot_posts_count", "-posts_count", "-profiles_count")
