from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
import phonenumbers



class UserSerializer(serializers.ModelSerializer):
    group = serializers.CharField()

    def create(self, validated_data):
        group_data = validated_data.pop("group")
        photo_data = validated_data.pop("photo", None)
        group, _ = Group.objects.get_or_create(name=group_data)
        user = self.Meta.model.objects.create_user(**validated_data)
        user.groups.add(group)
        user.photo = photo_data
        user.save()
        return user

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

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        phone = phonenumbers.parse(data, "CO")
        return phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)


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


