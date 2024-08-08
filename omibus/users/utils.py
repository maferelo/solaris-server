from django.conf import settings
from twilio.base.exceptions import TwilioRestException

from .twilio_client import client


def check_code(phone, code):
    try:
        return (
            client.verify.services(settings.TWILIO_SERVICE_SID).verification_checks.create(to=phone, code=code).status
            == "approved"
        )
    except TwilioRestException:
        return False
