"""
rollsocialnetwork views
"""
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.conf import settings
from django.contrib.auth import logout

class LogoutView(View):
    """
    logout view
    """
    def get(self, request):
        """
        get
        """
        logout(request)
        return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)
