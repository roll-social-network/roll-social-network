"""
rollsocialnetwork fields
"""
from django import forms
from django.conf import settings
from .widgets import SubdomainInput

class RollDomainField(forms.CharField):
    """
    roll domain field
    """

    widget = SubdomainInput(settings.SUBDOMAIN_BASE)

    def to_python(self, value):
        return f"{value}.{settings.SUBDOMAIN_BASE}"
