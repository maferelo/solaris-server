"""
ASGI config for omibus project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

asgi_application = get_asgi_application()

from omibus.trips.consumers import TripsConsumer  # noqa: E402
from omibus.trips.middleware import TokenAuthMiddlewareStack  # noqa: E402

# If DJANGO_SETTINGS_MODULE is unset, default to the local settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

# This application object is used by any ASGI server configured to use this file.
application = ProtocolTypeRouter(
    {
        "http": asgi_application,
        "websocket": TokenAuthMiddlewareStack(
            URLRouter(
                [
                    path("trip/", TripsConsumer.as_asgi()),
                ]
            )
        ),
    },
)
# Apply ASGI middleware here.
# from helloworld.asgi import HelloWorldApplication
# application = HelloWorldApplication(application)
