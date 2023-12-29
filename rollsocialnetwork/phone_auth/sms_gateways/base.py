"""
phone auth sms gateways base
"""
from typing import (
    TYPE_CHECKING,
    Optional
)

if TYPE_CHECKING:
    from rollsocialnetwork.phone_auth.models import VerificationCode

class SMSGatewayBase:  # pylint: disable=R0903
    """
    sms gateway base
    """
    key: Optional[str] = None

    def __init__(self, *args) -> None:
        pass

    def send(self, verification_code: "VerificationCode") -> None:
        """
        send
        """
        raise NotImplementedError(f"Not Implemented {self.__class__.__name__}.send()")
