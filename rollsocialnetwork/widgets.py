"""
rollsocialnetwork widgets
"""
from django.forms import widgets

class SubdomainInput(widgets.Input):
    """
    subdomain input
    """

    input_type = "text"
    template_name = "forms/widgets/subdomain.html"

    def __init__(self, subdomain, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.subdomain = subdomain

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["subdomain"] = self.subdomain
        return context
