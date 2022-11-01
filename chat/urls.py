from django.urls import path

from . import views


urlpatterns = [
    path("", views.Home.as_view(), name='home'),
    path("api/v1/user/", views.ListUser.as_view(), name="list_user"),
]
