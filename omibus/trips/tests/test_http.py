from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from omibus.users.tests.constants import PASSWORD
from omibus.users.tests.utils import create_user

from ..models import Trip


class HttpTripTest(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.driver = create_user(phone="+573017839877", group_name="driver")
        self.user_without_group = create_user(phone="+573017839878", group_name="")
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

    def test_driver_can_retrieve_trip_by_id(self):
        trip = Trip.objects.create(pick_up_address="A", drop_off_address="B", driver=self.driver)
        self.client.login(username=self.driver.phone, password=PASSWORD)
        response = self.client.get(trip.get_absolute_url())
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(str(trip.id), response.data.get("id"))

    def test_user_without_group_cannot_retrieve_trip_by_id(self):
        trip = Trip.objects.create(pick_up_address="A", drop_off_address="B", rider=self.user_without_group)
        self.client.login(username=self.user_without_group.phone, password=PASSWORD)
        response = self.client.get(trip.get_absolute_url())
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_trip_str_returns_id(self):
        trip = Trip.objects.create(pick_up_address="A", drop_off_address="B")
        self.assertEqual(str(trip.id), str(trip))
