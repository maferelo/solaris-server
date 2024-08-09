from rest_framework.test import APITestCase

from omibus.users.tasks import send_code


class SendCodeTest(APITestCase):
    def test_send_code(self):
        send_code(phone="+573017839876")
