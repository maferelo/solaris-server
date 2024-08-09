from django.conf import settings
from twilio.rest import Client


class FakeVerificationCheckInstance:
    def __init__(self, *args, **kwargs):
        self.status = "approved"


class FakeVerificationList:
    @staticmethod
    def create(*args, **kwargs):
        return


class FakeVerificationChecks:
    @staticmethod
    def create(*args, **kwargs):
        return FakeVerificationCheckInstance()


class FakeServices:
    def __init__(self, *args, **kwargs):
        self.verifications = FakeVerificationList()
        self.verification_checks = FakeVerificationChecks()


class FakeClient:
    def __init__(self, *args, **kwargs):
        self.verify = self.Verify()

    class Verify:
        @staticmethod
        def services(*args, **kwargs):
            return FakeServices()


if True:
    client = FakeClient()
else:
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
