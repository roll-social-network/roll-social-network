"""
phone auth sms gateways
"""
from typing import (
    Dict,
    Type,
)
from django.conf import settings
from .base import SMSGatewayBase
from .disabled import DisabledGateway
from .logger import LoggerGateway
from .twilio import TwilioGateway

GATEWAYS: Dict[str, Type[SMSGatewayBase]] = {}

def register(clss: Type[SMSGatewayBase]) -> None:
    """
    register
    """
    assert clss.key, f"Requires name field in {clss.__name__} class"
    GATEWAYS[clss.key] = clss

def get_sms_gateway() -> SMSGatewayBase:
    """
    get sms gateway
    """
    gateway_clss = GATEWAYS.get(settings.PHONE_AUTH_SMS_GATEWAY)
    assert gateway_clss, f"invalid phone auth gateway '{settings.PHONE_AUTH_SMS_GATEWAY}'"
    return gateway_clss(*settings.PHONE_AUTH_SMS_GATEWAY_ARGS)

register(LoggerGateway)
register(DisabledGateway)
register(TwilioGateway)
