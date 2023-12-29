"""
phone auth sms gateway logger
"""
import logging
from typing import TYPE_CHECKING
from .base import SMSGatewayBase

if TYPE_CHECKING:
    from rollsocialnetwork.phone_auth.models import VerificationCode

logger = logging.getLogger(__name__)

class LoggerGateway(SMSGatewayBase):  # pylint: disable=R0903
    """
    logger gateway

    4dev! log stream shows phone verification code
    """
    key = "logger"

    def __init__(self, level: (int | str)=logging.WARNING) -> None:
        self.level = int(level)

    def send(self, verification_code: "VerificationCode") -> None:
        logger.log(self.level,
                   "[SMSGateway.logger] %s verification code is %s",
                   verification_code.user,
                   verification_code.code)
