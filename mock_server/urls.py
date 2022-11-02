from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    # api urls
    path("api/v1/user/", views.ListUser.as_view(), name="list_user"),
    path("api/v1/message/", views.MessageList.as_view(), name="conversation"),
    path(
        "api/v1/message/<int:id>/", views.MessageDetail.as_view(), name="get_user_by_id"
    ),
]
