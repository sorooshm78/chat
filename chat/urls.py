from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r"message", views.MessageModelViewSet, basename="message-api")

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("api/v1/user/", views.ListUser.as_view(), name="list_user"),
    path("api/v1/", include(router.urls)),
]
