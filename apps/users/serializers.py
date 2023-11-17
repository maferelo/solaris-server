from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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


class LogInSerializer(TokenObtainPairSerializer):  # new
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = UserSerializer(user).data
        for key, value in user_data.items():
            if key != "id":
                token[key] = value
        return token
