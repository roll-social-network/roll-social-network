"""
rollsocialnetwork context processors
"""
from django.conf import settings

def is_home_site(request):
    """
    is home site?
    """
    return {"is_home_site": request.site.id == settings.HOME_SITE_ID}
