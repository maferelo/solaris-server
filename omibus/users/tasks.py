from celery import shared_task
from django.conf import settings

from .twilio_client import client


@shared_task()
def send_code(phone):
    client.verify.services(settings.TWILIO_SERVICE_SID).verifications.create(to=phone, channel="sms")
