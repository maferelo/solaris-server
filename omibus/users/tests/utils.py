from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from twilio.base.exceptions import TwilioRestException

from .constants import PASSWORD


def create_user(phone="+573017839876", password=PASSWORD, group_name="rider"):
    group, _ = Group.objects.get_or_create(name=group_name)
    user = get_user_model().objects.create_user(phone=phone, password=password)
    user.groups.add(group)
    user.save()
    return user


class FakeTwilioClientRaisesException:
    def __init__(self, *args, **kwargs):
        self.verify = self.Verify()

    class Verify:
        @staticmethod
        def services(*args, **kwargs):
            raise TwilioRestException(status=400, uri="uri")


fake_twilio_client_raises_exception = FakeTwilioClientRaisesException()
