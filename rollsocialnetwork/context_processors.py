"""
rollsocialnetwork context processors
"""
from django.conf import settings
from django.contrib.sites.models import Site
from .utils import get_popular_rolls

def home_site(request):
    """
    adds home_site and is_home_site
    """
    site = None
    try:
        site = Site.objects.get(id=settings.HOME_SITE_ID)
    except Site.DoesNotExist:
        pass
    return {
        "home_site": site,
        "is_home_site": request.site.id == settings.HOME_SITE_ID
    }

def another_rolls(request):
    """
    another rolls
    """
    if not request.user.is_authenticated:
        return {"another_rolls": []}
    qs = Site.objects.exclude(id__in=[settings.HOME_SITE_ID,
                                      request.site.id]).filter(profiles__user=request.user)
    return {"another_rolls": get_popular_rolls(qs)}
