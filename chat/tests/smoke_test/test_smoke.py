from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APIClient


class SmokeTest(TestCase):
    def setUp(self):
        # Client 1 Setup
        self.user1 = User.objects.create(username="user1", password="a/@1234567")
        self.client1 = APIClient()
        self.client1.force_login(self.user1)

        # Client 2 Setup
        self.user2 = User.objects.create(username="user2", password="a/@1234567")
        self.client2 = APIClient()
        self.client2.force_login(self.user2)

        # Urls
        self.list_user_url = reverse("list_user")
        # self.list_message_url = reverse("list_create_message")
        # self.detail_message_url = reverse("detail_message")

    def test_diffrent_send_request_from_client1_and_client2(self):
        response1 = self.client1.get(self.list_user_url)
        response2 = self.client2.get(self.list_user_url)

        self.assertNotEqual(response1.data, response2.data)
