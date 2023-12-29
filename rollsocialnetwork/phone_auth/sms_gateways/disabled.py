"""
phone auth sms gateway logger
"""
from typing import TYPE_CHECKING
from .base import SMSGatewayBase

if TYPE_CHECKING:
    from rollsocialnetwork.phone_auth.models import VerificationCode

class DisabledGateway(SMSGatewayBase):  # pylint: disable=R0903
    """
    disabled gateway
    """
    key = "disabled"

    def send(self, verification_code: "VerificationCode") -> None:
        pass
