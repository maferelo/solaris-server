from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import log_in_view, send_code_view

app_name = "users"
urlpatterns = [
    path("log-in/", log_in_view, name="log_in"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("send-code/", send_code_view, name="send_code"),
]
urlpatterns = [path("auth/", include(urlpatterns))]
