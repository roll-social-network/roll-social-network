"""
phone auth admin
"""
from django.contrib import admin
from .models import (
    VerificationCode,
    OTPSecret,
)

class VerificationCodeAdmin(admin.ModelAdmin):
    """
    VerificationCode model admin
    """
    fields = [
        "user",
        "attempts",
        "valid_until",
    ]
    readonly_fields = [
        "attempts",
        "valid_until",
    ]

class OTPSecretAdmin(admin.ModelAdmin):
    """
    OTP Secret model admin
    """

    fields = []
    readonly_fields = ["user"]

admin.site.register(VerificationCode, VerificationCodeAdmin)
admin.site.register(OTPSecret, OTPSecretAdmin)
