"""
phone auth context processors
"""
from .models import OTPSecret

def otp_secret_validated(request):
    """
    otp secret validated
    """
    if not request.user.is_authenticated:
        return {"otp_secret_validated": False}
    qs = OTPSecret.objects.filter(user=request.user,
                                  valid_at__isnull=False)
    return {"otp_secret_validated": qs.exists()}
