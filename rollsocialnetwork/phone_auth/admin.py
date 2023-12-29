"""
phone auth admin
"""
from django.contrib import admin
from .models import VerificationCode

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

admin.site.register(VerificationCode, VerificationCodeAdmin)
