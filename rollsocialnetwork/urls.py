"""
URL configuration for rollsocialnetwork project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""
from django.conf import settings
from django.contrib import admin
from django.urls import (
    path,
    include,
    re_path,
)
from django.views.static import serve
from .opener_callback import OpenerCallbackView
from .views import (
    LogoutView,
    NginxAccelRedirectView,
    HomeView,
    RollsView,
    CreateRollView,
    LoginView,
)

urlpatterns = [
    path("",
         HomeView.as_view(),
         name="home"),
    path("rolls/",
         RollsView.as_view(),
         name="rolls"),
    path("create-roll/",
         CreateRollView.as_view(),
         name="create-roll"),
    path("phone-auth/",
         include("rollsocialnetwork.phone_auth.urls",
                 namespace="phoneauth")),
    path("callback/opener/",
         OpenerCallbackView.as_view(),
         name="opener_callback"),
    path("login/",
         LoginView.as_view(),
         name="login"),
    path("logout/",
         LogoutView.as_view(),
         name="logout"),
    path("s/",
         include("rollsocialnetwork.social.urls")),
    path("t/",
         include("rollsocialnetwork.timeline.urls")),
    path("oauth2/",
         include("oauth2_provider.urls",
                 namespace="oauth2")),
    path("admin/",
         admin.site.urls),
]

if settings.MEDIA_PATH_AS_STATIC:
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {
                "document_root": settings.MEDIA_ROOT,
            },
        ),
    ]

if settings.MEDIA_PATH_AS_NGINX_ACCEL:
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            NginxAccelRedirectView.as_view()
        )
    ]
