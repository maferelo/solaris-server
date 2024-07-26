from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from .views import send_code_view, log_in_view

app_name = "users"
urlpatterns = [
    path("log_in/", log_in_view, name="log_in"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("send_code/", send_code_view, name="send_code"),
]
urlpatterns = [path("auth/", include(urlpatterns))]
