import pytest
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework_simplejwt.tokens import AccessToken

from config.asgi import application

from ..models import Trip

TEST_CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}


@database_sync_to_async
def create_trip(
    pick_up_address="123 Main Street", drop_off_address="456 Piney Road", status="REQUESTED", rider=None, driver=None
):
    return Trip.objects.create(
        pick_up_address=pick_up_address, drop_off_address=drop_off_address, status=status, rider=rider, driver=driver
    )


@database_sync_to_async
def create_user(phone, password, group="rider", is_active=True):
    # Create user.
    user = get_user_model().objects.create_user(phone=phone, password=password, is_active=is_active)

    # Create user group.
    user_group, _ = Group.objects.get_or_create(name=group)  # new
    user.groups.add(user_group)
    user.save()

    # Create access token.
    access = AccessToken.for_user(user)
    return user, access


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestWebSocket:
    async def test_can_connect_to_server(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user("+000000000", "pAssw0rd")
        communicator = WebsocketCommunicator(application=application, path=f"/trip/?token={access}")
        connected, _ = await communicator.connect()
        assert connected is True
        await communicator.disconnect()

    async def test_request_trip_with_inactive_user(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        user, access = await create_user("+000000000", "pAssw0rd", "driver", is_active=False)
        communicator = WebsocketCommunicator(application=application, path=f"/trip/?token={access}")
        await communicator.connect()
        await communicator.send_json_to(
            {
                "type": "create.trip",
                "data": {
                    "pick_up_address": "123 Main Street",
                    "drop_off_address": "456 Piney Road",
                    "rider": user.id,
                },
            }
        )
        response = await communicator.receive_json_from()
        response_data = response.get("data")
        assert response_data["id"] is not None
        assert response_data["pick_up_address"] == "123 Main Street"
        assert response_data["drop_off_address"] == "456 Piney Road"
        assert response_data["status"] == "REQUESTED"
        assert response_data["rider"]["phone"] == user.phone
        assert response_data["driver"] is None
        await communicator.disconnect()

    async def test_request_trip_with_anonymous_user(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        user, access = await create_user("+000000000", "pAssw0rd", "driver")
        communicator = WebsocketCommunicator(application=application, path="/trip/?token=invalid-token")
        await communicator.connect()
        await communicator.send_json_to(
            {
                "type": "create.trip",
                "data": {
                    "pick_up_address": "123 Main Street",
                    "drop_off_address": "456 Piney Road",
                    "rider": user.id,
                },
            }
        )
        response = await communicator.receive_json_from()
        response_data = response.get("data")
        assert response_data["id"] is not None
        assert response_data["pick_up_address"] == "123 Main Street"
        assert response_data["drop_off_address"] == "456 Piney Road"
        assert response_data["status"] == "REQUESTED"
        assert response_data["rider"]["phone"] == user.phone
        assert response_data["driver"] is None
        await communicator.disconnect()

    async def test_can_send_and_receive_messages(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user("+000000000", "pAssw0rd")
        communicator = WebsocketCommunicator(application=application, path=f"/trip/?token={access}")
        await communicator.connect()
        message = {
            "type": "echo.message",
            "data": "This is a test message.",
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_can_send_and_receive_broadcast_messages(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user("+000000000", "pAssw0rd")
        communicator = WebsocketCommunicator(application=application, path=f"/trip/?token={access}")
        await communicator.connect()
        message = {
            "type": "echo.message",
            "data": "This is a test message.",
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send("test", message=message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_cannot_connect_to_socket(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(application=application, path="/trip/")
        connected, _ = await communicator.connect()
        assert connected is False
        await communicator.disconnect()

    async def test_join_driver_pool(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user("+000000000", "pAssw0rd", "driver")
        communicator = WebsocketCommunicator(application=application, path=f"/trip/?token={access}")
        await communicator.connect()
        message = {
            "type": "echo.message",
            "data": "This is a test message.",
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send("drivers", message=message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_request_trip(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        user, access = await create_user("+000000000", "pAssw0rd", "driver")
        communicator = WebsocketCommunicator(application=application, path=f"/trip/?token={access}")
        await communicator.connect()
        await communicator.send_json_to(
            {
                "type": "create.trip",
                "data": {
                    "pick_up_address": "123 Main Street",
                    "drop_off_address": "456 Piney Road",
                    "rider": user.id,
                },
            }
        )
        response = await communicator.receive_json_from()
        response_data = response.get("data")
        assert response_data["id"] is not None
        assert response_data["pick_up_address"] == "123 Main Street"
        assert response_data["drop_off_address"] == "456 Piney Road"
        assert response_data["status"] == "REQUESTED"
        assert response_data["rider"]["phone"] == user.phone
        assert response_data["driver"] is None
        await communicator.disconnect()

    async def test_create_trip_group(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        user, access = await create_user("+000000000", "pAssw0rd", "rider")
        communicator = WebsocketCommunicator(application=application, path=f"/trip/?token={access}")
        await communicator.connect()

        # Send a ride request.
        await communicator.send_json_to(
            {
                "type": "create.trip",
                "data": {
                    "pick_up_address": "123 Main Street",
                    "drop_off_address": "456 Piney Road",
                    "rider": user.id,
                },
            }
        )
        response = await communicator.receive_json_from()
        response_data = response.get("data")

        # Send a message to the trip group.
        message = {
            "type": "echo.message",
            "data": "This is a test message.",
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send(response_data["id"], message=message)

        # Rider receives message.
        response = await communicator.receive_json_from()
        assert response == message

        await communicator.disconnect()

    async def test_join_trip_group_on_connect(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        user, access = await create_user("+000000000", "pAssw0rd", "rider")
        trip = await create_trip(rider=user)
        communicator = WebsocketCommunicator(application=application, path=f"/trip/?token={access}")
        connected, _ = await communicator.connect()

        # Send a message to the trip group.
        message = {
            "type": "echo.message",
            "data": "This is a test message.",
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send(f"{trip.id}", message=message)

        # Rider receives message.
        response = await communicator.receive_json_from()
        assert response == message

        await communicator.disconnect()

    async def test_driver_can_update_trip(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS

        # Create trip request.
        rider, _ = await create_user("+000000000", "pAssw0rd", "rider")
        trip = await create_trip(rider=rider)
        trip_id = f"{trip.id}"

        # Listen for messages as rider.
        channel_layer = get_channel_layer()
        await channel_layer.group_add(group=trip_id, channel="test_channel")

        # Update trip.
        driver, access = await create_user("+000000001", "pAssw0rd", "driver")
        communicator = WebsocketCommunicator(application=application, path=f"/trip/?token={access}")
        await communicator.connect()
        message = {
            "type": "update.trip",
            "data": {
                "id": trip_id,
                "pick_up_address": trip.pick_up_address,
                "drop_off_address": trip.drop_off_address,
                "status": Trip.IN_PROGRESS,
                "driver": driver.id,
            },
        }
        await communicator.send_json_to(message)

        # Rider receives message.
        response = await channel_layer.receive("test_channel")
        response_data = response.get("data")
        assert response_data["id"] == trip_id
        assert response_data["rider"]["phone"] == rider.phone
        assert response_data["driver"]["phone"] == driver.phone

        await communicator.disconnect()

    async def test_driver_join_trip_group_on_connect(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        user, access = await create_user("+000000000", "pAssw0rd", "driver")
        trip = await create_trip(driver=user)
        communicator = WebsocketCommunicator(application=application, path=f"/trip/?token={access}")
        await communicator.connect()

        # Send a message to the trip group.
        message = {
            "type": "echo.message",
            "data": "This is a test message.",
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send(f"{trip.id}", message=message)

        # Rider receives message.
        response = await communicator.receive_json_from()
        assert response == message

        await communicator.disconnect()
