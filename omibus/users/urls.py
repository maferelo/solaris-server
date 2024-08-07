from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import log_in_view, send_code_view

app_name = "users"
urlpatterns = [
    path("log_in/", log_in_view, name="log-in"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("send_code/", send_code_view, name="send-code"),
]
urlpatterns = [path("auth/", include(urlpatterns))]
