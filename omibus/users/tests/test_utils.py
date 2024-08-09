from unittest.mock import patch

from rest_framework.test import APITestCase

from omibus.users.utils import check_code

from .utils import fake_twilio_client_raises_exception


class SendCodeTest(APITestCase):
    @patch("omibus.users.utils.client", fake_twilio_client_raises_exception)
    def test_when_check_code_client_fails(self):
        response = check_code("+573017839876", "123456")
        self.assertEqual(response, False)
