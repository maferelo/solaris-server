from django.urls import path
from trips.views import TripView

app_name = "trips"
urlpatterns = [
    path("", TripView.as_view({"get": "list"}), name="trip_list"),
]
