from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),

    # api urls
    path("api/v1/user/", views.ListUser.as_view(), name="list_user"),
]