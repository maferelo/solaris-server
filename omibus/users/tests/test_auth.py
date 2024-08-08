from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

CODE = "123456"
PASSWORD = "pAssw0rd!"


def create_user(phone="+573017839876", password=PASSWORD, group_name="rider"):
    group, _ = Group.objects.get_or_create(name=group_name)
    user = get_user_model().objects.create_user(phone=phone, password=password)
    user.groups.add(group)
    user.save()
    return user


class SendCodeTest(APITestCase):
    @patch("omibus.users.views.send_code")
    def test_user_can_request_code(self, send_code):
        user = create_user()
        send_code.return_value = None
        response = self.client.post(
            reverse("users:send_code"),
            data={
                "phone": user.phone,
            },
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    @patch("omibus.users.views.send_code")
    def test_user_cannot_request_code_with_invalid_phone(self, send_code):
        send_code.return_value = None
        response = self.client.post(
            reverse("users:send_code"),
            data={
                "phone": "abcd",
            },
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class AuthenticationTest(APITestCase):
    @patch("omibus.users.auth_backend.check_code")
    def test_user_can_log_in(self, mock_check_code):
        user = create_user()
        mock_check_code.return_value = True
        response = self.client.post(
            reverse("users:log_in"),
            data={
                "phone": user.phone,
                "code": CODE,
            },
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data["refresh"])

    @patch("omibus.users.auth_backend.check_code")
    def test_user_cannot_log_in_with_invalid_code(self, mock_check_code):
        user = create_user()
        mock_check_code.return_value = False
        response = self.client.post(
            reverse("users:log_in"),
            data={
                "phone": user.phone,
                "code": CODE,
            },
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
