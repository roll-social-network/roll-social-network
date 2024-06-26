"""
uris templatetags
"""
from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.urls import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def site_build_absolute_uri(context,
                            site: Site,
                            viewname: str,
                            **kwargs: dict[str, int|str]) -> str:
    """
    site build absolute uri

    {% site_build_absolute_uri site "url_name" %}
    """
    path = reverse(viewname, kwargs=kwargs)
    if site and context.request.site.pk == site.pk:
        return path
    scheme = settings.OVERRIDE_SCHEME or context.request.scheme
    return f"{scheme}://{site.domain}{path}"
