from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..models import Trip

PASSWORD = "pAssw0rd!"


def create_user(phone="+3017839876", password=PASSWORD, group_name="rider"):
    group, _ = Group.objects.get_or_create(name=group_name)
    user = get_user_model().objects.create_user(phone=phone, password=password)
    user.groups.add(group)
    user.save()
    return user


class HttpTripTest(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client.login(username=self.user.phone, password=PASSWORD)

    def test_user_can_list_trips(self):
        trips = [
            Trip.objects.create(pick_up_address="A", drop_off_address="B", rider=self.user),
            Trip.objects.create(pick_up_address="B", drop_off_address="C", rider=self.user),
            Trip.objects.create(pick_up_address="C", drop_off_address="D"),
        ]
        response = self.client.get(reverse("trips:trip_list"))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        exp_trip_ids = [str(trip.id) for trip in trips[0:2]]
        act_trip_ids = [trip.get("id") for trip in response.data]
        self.assertCountEqual(act_trip_ids, exp_trip_ids)

    def test_user_can_retrieve_trip_by_id(self):
        trip = Trip.objects.create(pick_up_address="A", drop_off_address="B", rider=self.user)
        response = self.client.get(trip.get_absolute_url())
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(str(trip.id), response.data.get("id"))
