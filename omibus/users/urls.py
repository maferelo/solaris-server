from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginView, SendCodeView

app_name = "users"
urlpatterns = [
    path("log-in/", LoginView.as_view(), name="log_in"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("send-code/", SendCodeView.as_view(), name="send_code"),
]
urlpatterns = [path("auth/", include(urlpatterns))]
