"""
URL configuration for rollsocialnetwork project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""

from django.contrib import admin
from django.urls import (
    path,
    include,
)
from django.views.generic import TemplateView
from .views import LogoutView

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path("phone-auth/", include("rollsocialnetwork.phone_auth.urls")),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("s/", include("rollsocialnetwork.social.urls")),
    path("admin/", admin.site.urls),
]
