import base64
import json

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

PASSWORD = "pAssw0rd!"


def create_user(phone="+3017839876", password=PASSWORD):
    return get_user_model().objects.create_user(phone=phone, password=password)


class AuthenticationTest(APITestCase):
    def test_user_can_sign_up(self):
        response = self.client.post(
            reverse("users:sign_up"),
            data={
                "phone": "+573017839876",
            },
        )
        user = get_user_model().objects.last()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data["id"], user.id)
        self.assertEqual(response.data["phone"], user.phone)

    def test_user_can_log_in(self):  # new
        user = create_user()
        response = self.client.post(
            reverse("users:log_in"),
            data={
                "phone": user.phone,
                "password": PASSWORD,
            },
        )

        # Parse payload data from access token.
        access = response.data["access"]
        header, payload, signature = access.split(".")
        decoded_payload = base64.b64decode(f"{payload}==")
        payload_data = json.loads(decoded_payload)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data["refresh"])
        self.assertEqual(payload_data["id"], user.id)
        self.assertEqual(payload_data["phone"], user.phone)
