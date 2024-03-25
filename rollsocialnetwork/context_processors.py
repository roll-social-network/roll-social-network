"""
rollsocialnetwork context processors
"""
from django.conf import settings

def is_home_site(request):
    """
    is home site?
    """
    return {"is_home_site": request.site.id == settings.HOME_SITE_ID}

def footer_urls(request):
    """
    footer urls
    """
    return {
        "about_page_url": settings.ABOUT_PAGE_URL,
        "terms_page_url": settings.TERMS_PAGE_URL
    }
