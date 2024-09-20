from unittest.mock import patch

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from omibus.users.auth_backend import PasswordlessAuthBackend

from .constants import CODE
from .utils import create_user


class SuperUserTest(APITestCase):
    def test_create_superuser(self):
        super_user = get_user_model().objects.create_superuser(phone="+573017839876", password="password")
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_admin)

    def test_create_superuser_without_phone(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(phone=None, password="password")


class AuthenticationTest(APITestCase):
    def test_user_can_request_code(self):
        user = create_user()
        response = self.client.post(
            reverse("users:send_code"),
            data={
                "phone": user.phone,
            },
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_cannot_request_code_with_invalid_phone(self):
        response = self.client.post(
            reverse("users:send_code"),
            data={
                "phone": "abcd",
            },
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_user_can_log_in(self):
        user = create_user()
        response = self.client.post(
            reverse("users:log_in"),
            data={
                "phone": user.phone,
                "code": CODE,
                "group": "rider",
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
                "code": "abcd",
            },
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        response = self.client.post(
            reverse("users:log_in"),
            data={
                "phone": user.phone,
                "code": CODE,
                "group": "rider",
            },
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_authenticate_new_user(self):
        auth_backend = PasswordlessAuthBackend()
        user = auth_backend.authenticate("", phone="+573017839876", code=CODE)
        self.assertEqual(user.phone, "+573017839876")

    def test_get_user_that_exists(self):
        user = create_user()
        auth_backend = PasswordlessAuthBackend()
        user = auth_backend.get_user(user.pk)
        self.assertEqual(user.phone, "+573017839876")

    def test_get_user_that_does_not_exist(self):
        auth_backend = PasswordlessAuthBackend()
        user = auth_backend.get_user(1)
        self.assertIsNone(user)
