from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        if not phone:
            raise ValueError("Users must have a phone number")

        user = self.model(phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password):
        user = self.create_user(phone=phone, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None
    last_name = None
    phone_validator = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone = models.TextField(
        max_length=15,
        unique=True,
        blank=False,
        help_text="Required. 15 characters or fewer. Digits only.",
        validators=[phone_validator],
        error_messages={
            "unique": "A user with that phone number already exists.",
        },
    )

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    @property
    def group(self):
        groups = self.groups.all()
        return groups[0].name if groups else None
