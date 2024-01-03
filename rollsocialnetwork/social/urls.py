"""
social urls
"""
from django.urls import path
from .views import (
    TimelineView,
    UserProfileDetailView,
    UserProfileCreateView,
)

urlpatterns = [
    path("", TimelineView.as_view(), name="social-timeline"),
    path("create-user-profile/",
         UserProfileCreateView.as_view(),
         name='social-create-user-profile'),
    path("<str:username>/", UserProfileDetailView.as_view(), name="social-user-profile"),
]
