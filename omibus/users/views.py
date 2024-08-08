from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .exceptions import InvalidCode
from .serializers import LogInSerializer, SendCodeSerializer
from .tasks import send_code


class SendCodeView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    @extend_schema(request=SendCodeSerializer)
    def post(self, request):
        serializer = SendCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_code.delay(phone=serializer.validated_data.get("phone"))
        return Response()


class LoginView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    @extend_schema(request=LogInSerializer, responses=TokenObtainPairSerializer)
    def post(self, request):
        serializer = LogInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(phone=serializer.validated_data.get("phone"), code=serializer.validated_data.get("code"))
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            )
        else:
            raise InvalidCode()
