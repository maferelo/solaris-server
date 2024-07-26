from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .utils import check_code


class PasswordlessAuthBackend(ModelBackend):
    def authenticate(self, phone=None, code=None):
        user_model = get_user_model()
        if check_code(phone, code):
            try:
                return user_model.objects.get(phone=phone)
            except user_model.DoesNotExist:
                return user_model.objects.create_user(phone=phone)
        return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
