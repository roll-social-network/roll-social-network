"""
phone auth admin
"""
from django.contrib import admin
from .models import VerificationCode

class VerificationCodeAdmin(admin.ModelAdmin):
    """
    VerificationCode model admin
    """
    readonly_fields = [
        "code",
        "valid_until",
    ]

admin.site.register(VerificationCode, VerificationCodeAdmin)
