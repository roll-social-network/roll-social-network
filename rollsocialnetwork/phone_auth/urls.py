"""
phone auth urls
"""
from django.urls import path
from .views import (
    RequestVerificationCodeView,
    VerifyVerificationCodeView,
    ShowOTPSecretView,
)

urlpatterns = [
    path("request/",
         RequestVerificationCodeView.as_view(),
         name="request-verification-code"),
    path("verify/",
         VerifyVerificationCodeView.as_view(),
         name="verify-verification-code"),
    path("show-otp-secret/", ShowOTPSecretView.as_view()),
]
