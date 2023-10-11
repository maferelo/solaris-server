from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "phone",
        )
        read_only_fields = ("id",)


class LogInSerializer(TokenObtainPairSerializer):  # new
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = UserSerializer(user).data
        for key, value in user_data.items():
            if key != "id":
                token[key] = value
        return token
