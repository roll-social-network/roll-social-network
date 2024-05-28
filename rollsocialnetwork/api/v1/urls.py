"""
api.v1 urls
"""
from django.urls import path
from .router import router
from .views import (
    LoginView,
    RequestVerificationCodeView,
    VerifyVerificationCodeView,
    OAuth2AuthorizeView,
)

app_name = "v1"

urlpatterns = [
    path("login/",
         LoginView.as_view(),
         name="login"),
    path("request-verification-code/",
         RequestVerificationCodeView.as_view(),
         name="request-verification-code"),
    path("verify-verification-code/",
         VerifyVerificationCodeView.as_view(),
         name="verify-verification-code"),
    path("oauth2/authorize/",
         OAuth2AuthorizeView.as_view(),
         name="oauth2_authorize"),
] + router.urls
