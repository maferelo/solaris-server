import phonenumbers
from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    group = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = ("id", "phone", "group", "photo")
        read_only_fields = ("id",)


class PhoneSerializer(serializers.CharField):
    @staticmethod
    def _validate_phone(value):
        try:
            phone = phonenumbers.parse(value, "CO")
            phonenumbers.is_valid_number(phone)
        except phonenumbers.phonenumberutil.NumberParseException:
            raise serializers.ValidationError("Invalid phone number")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(self._validate_phone)

    def run_validation(self, *args, **kwargs):
        value = super().run_validation(*args, **kwargs)
        return phonenumbers.format_number(phonenumbers.parse(value, "CO"), phonenumbers.PhoneNumberFormat.E164)


class CodeSerializer(serializers.CharField):
    @staticmethod
    def _validate_code(value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("Invalid code")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(self._validate_code)


class SendCodeSerializer(serializers.Serializer):
    phone = PhoneSerializer()


class LogInSerializer(serializers.Serializer):
    phone = PhoneSerializer()
    code = CodeSerializer()
