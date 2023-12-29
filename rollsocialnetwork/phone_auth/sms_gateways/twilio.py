"""
phone auth sms gateway twilio
"""
import logging
from typing import TYPE_CHECKING
from twilio.rest import Client as Twilio
from .base import SMSGatewayBase

if TYPE_CHECKING:
    from rollsocialnetwork.phone_auth.models import VerificationCode

logger = logging.getLogger(__name__)

class TwilioGateway(SMSGatewayBase):  # pylint: disable=R0903
    """
    twilio gateway
    """
    key = "twilio"

    def __init__(self,
                 api_key: str,
                 api_secret: str,
                 account_sid: str,
                 messaging_service_sid: str) -> None:
        self.twilio_client = Twilio(api_key,
                                    api_secret,
                                    account_sid)
        self.twilio_messaging_service_sid = messaging_service_sid

    def send(self, verification_code: "VerificationCode") -> None:
        self.twilio_client.messages.create(
            to=verification_code.user.get_username(),
            messaging_service_sid=self.twilio_messaging_service_sid,
            body=self.build_message_body(verification_code)
        )
