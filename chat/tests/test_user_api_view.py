from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status

from ..serializers import UserModelSerializer


class TestUserApiView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("list_user")
        self.user1 = User.objects.create(username="user1", password="a/@1234567")
        self.user2 = User.objects.create(username="user2", password="a/@1234567")
        self.user3 = User.objects.create(username="user3", password="a/@1234567")

    def test_get_users_without_authentication_403_status(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_users_200_status(self):
        # get API response
        self.client.force_login(self.user1)
        response = self.client.get(self.url)

        # get data from db
        users = User.objects.exclude(id=self.user1.id)
        serializer = UserModelSerializer(users, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
