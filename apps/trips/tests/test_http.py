from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from trips.models import Trip

PASSWORD = "pAssw0rd!"


def create_user(phone="+3017839876", password=PASSWORD):
    return get_user_model().objects.create_user(phone=phone, password=password)


class HttpTripTest(APITestCase):
    def setUp(self):
        user = create_user()
        response = self.client.post(
            reverse("users:log_in"),
            data={
                "phone": user.phone,
                "password": PASSWORD,
            },
        )
        self.access = response.data["access"]

    def test_user_can_list_trips(self):
        trips = [
            Trip.objects.create(pick_up_address="A", drop_off_address="B"),
            Trip.objects.create(pick_up_address="B", drop_off_address="C"),
        ]
        response = self.client.get(reverse("trips:trip_list"), headers={"authorization": f"Bearer {self.access}"})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        exp_trip_ids = [str(trip.id) for trip in trips]
        act_trip_ids = [trip.get("id") for trip in response.data]
        self.assertCountEqual(exp_trip_ids, act_trip_ids)
