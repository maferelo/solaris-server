from django.conf import settings

from .twilio_client import client


def check_code(phone, code):
    verification_check = client.verify.services(settings.TWILIO_SERVICE_SID).verification_checks.create(
        to=phone, code=code
    )

    return verification_check.status == "approved"
