from celery.exceptions import CeleryError
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from twilio.base.exceptions import TwilioRestException

from .serializers import LogInSerializer, SendCodeSerializer
from .tasks import send_code


@extend_schema(request=SendCodeSerializer)
@api_view(["POST"])
@authentication_classes(())
@permission_classes((AllowAny,))
def send_code_view(request):
    serializer = SendCodeSerializer(data=request.data)
    if serializer.is_valid():
        try:
            send_code.delay(phone=serializer.validated_data.get("phone"))
        except CeleryError:
            return Response({"detail": "Failed to send OTP"}, status=500)
        return Response({"detail": "OTP sent successfully"})
    return Response(serializer.errors, status=400)


@extend_schema(request=LogInSerializer, responses=TokenObtainPairSerializer)
@api_view(["POST"])
@authentication_classes(())
@permission_classes((AllowAny,))
def log_in_view(request):
    serializer = LogInSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = authenticate(
                phone=serializer.validated_data.get("phone"), code=serializer.validated_data.get("code")
            )
        except TwilioRestException:
            return Response({"detail": "Invalid OTP"}, status=400)

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=200,
        )
    return Response(serializer.errors, status=400)
