"""
phone_auth login methods
"""
from typing import List
from rollsocialnetwork.phone_auth.models import OTPSecret

VERIFICATION_CODE = "VERIFICATION_CODE"
OTP_CODE = "OTP_CODE"

METHODS = [
    VERIFICATION_CODE,
    OTP_CODE,
]

def available_methods(phone_number: str) -> List[str]:
    """
    get available login methods from phone number
    """
    login_methods = [VERIFICATION_CODE]
    if OTPSecret.phone_number_has_valid_otp_secret(phone_number):
        login_methods.append(OTP_CODE)
    return login_methods
