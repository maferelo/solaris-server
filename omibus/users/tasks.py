from celery import shared_task

from django.contrib.auth import get_user_model
from django.conf import settings
from .twilio_client import client


@shared_task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    user = get_user_model()
    return user.objects.count()


@shared_task()
def send_code(phone):
    verification = client.verify \
        .services(settings.TWILIO_SERVICE_SID) \
        .verifications \
        .create(to=phone, channel='sms')

    return verification.sid
