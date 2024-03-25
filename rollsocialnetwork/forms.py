"""
rollsocialnetwork forms
"""
from django import forms
from django.contrib.sites.models import Site
from .fields import RollDomainField

class RollForm(forms.ModelForm):
    """
    roll form
    """

    class Meta:
        model = Site
        fields = ["domain", "name"]

    domain = RollDomainField()
