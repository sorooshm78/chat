from django.urls import path

from . import views


urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("api/v1/user/", views.ListUser.as_view(), name="list_user"),
    path(
        "api/v1/message/", views.ListCreateMessage.as_view(), name="list_create_message"
    ),
]
