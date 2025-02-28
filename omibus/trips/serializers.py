from rest_framework import serializers

from omibus.users.serializers import UserSerializer

from .models import Trip


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"
        read_only_fields = (
            "id",
            "created",
            "updated",
        )


class NestedTripSerializer(serializers.ModelSerializer):
    driver = UserSerializer()
    rider = UserSerializer()

    class Meta:
        model = Trip
        fields = "__all__"
        depth = 1
