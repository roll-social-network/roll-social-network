"""
timeline urls
"""
from django.urls import path
from .views import (
    TimelineView,
    PostCreateView,
    PostLikeDislikeView,
)

urlpatterns = [
    path("", TimelineView.as_view(), name="timeline"),
    path("create-post/",
         PostCreateView.as_view(),
         name='timeline-create-post'),
    path("post/<int:pk>/like-dislike/",
         PostLikeDislikeView.as_view(),
         name='timeline-post-like-dislike'),
]
