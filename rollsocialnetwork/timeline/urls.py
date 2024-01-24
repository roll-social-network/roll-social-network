"""
timeline urls
"""
from django.urls import path
from .views import (
    TimelineView,
    PostCreateView,
)

urlpatterns = [
    path("", TimelineView.as_view(), name="timeline"),
    path("create-post/",
         PostCreateView.as_view(),
         name='timeline-create-post'),
]
