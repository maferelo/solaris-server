from django.db.models import Q
from rest_framework import permissions, viewsets

from .models import Trip
from .serializers import NestedTripSerializer


class TripView(viewsets.ReadOnlyModelViewSet):
    lookup_field = "id"
    lookup_url_kwarg = "trip_id"
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NestedTripSerializer

    def get_queryset(self):
        user = self.request.user
        if user.group == "driver":
            return Trip.objects.filter(Q(status=Trip.REQUESTED) | Q(driver=user))
        if user.group == "rider":
            return Trip.objects.filter(rider=user)
        return Trip.objects.none()
