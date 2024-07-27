from io import BytesIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

CODE = "123456"
PASSWORD = "pAssw0rd!"


def create_photo_file():
    data = BytesIO()
    Image.new("RGB", (100, 100)).save(data, "PNG")
    data.seek(0)
    return SimpleUploadedFile("photo.png", data.getvalue())


def create_user(phone="+573017839876", password=PASSWORD, group_name="rider"):
    group, _ = Group.objects.get_or_create(name=group_name)
    user = get_user_model().objects.create_user(phone=phone, password=password)
    user.groups.add(group)
    user.save()
    return user


class AuthenticationTest(APITestCase):
    @patch("users.auth_backend.check_code")
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
