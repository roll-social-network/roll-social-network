"""
social urls
"""
from django.urls import path
from .views import (
    UserProfileDetailView,
    UserProfileCreateView,
)

urlpatterns = [
    path("create-user-profile/",
         UserProfileCreateView.as_view(),
         name='social-create-user-profile'),
    path("<str:username>/", UserProfileDetailView.as_view(), name="social-user-profile"),
]
