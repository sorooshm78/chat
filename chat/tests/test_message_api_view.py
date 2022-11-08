from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework.test import APIClient
from rest_framework.response import Response
from rest_framework import status

from ..serializers import UserModelSerializer, MessageModelSerializer
from ..models import Message


class TestMessageApiView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.sender = User.objects.create(username="sender", password="a/@1234567")
        self.receiver = User.objects.create(username="receiver", password="a/@1234567")

        self.message = Message.objects.create(
            user=self.sender,
            recipient=self.receiver,
            body="test message",
        )

        self.list_create_url = reverse("list_create_message")
        self.detail_url = reverse("detail_message", kwargs={"pk": self.message.id})

    # List Message (GET)
    def test_get_list_message_200_status(self):
        # get API response
        self.client.force_login(self.sender)
        response = self.client.get(
            f"{self.list_create_url}?target={self.receiver.username}"
        )
        # get data from db
        messages = Message.objects.filter(
            Q(user=self.sender) | Q(user=self.receiver),
            Q(recipient=self.sender) | Q(recipient=self.receiver),
        )
        serializer = MessageModelSerializer(messages, many=True)
        db_data = {
            "results": serializer.data,
        }

        self.assertEqual(response.data, db_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_message_without_authentication_403_status(self):
        response = self.client.get(
            f"{self.list_create_url}?target={self.receiver.username}"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Create Message (POST)
    def test_post_message_201_status(self):
        data = {
            "recipient": self.receiver.username,
            "body": "test_post_message_201_status",
        }
        self.client.force_login(self.sender)
        response = self.client.post(self.list_create_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_message_by_empty_body_400_status(self):
        data = {
            "recipient": self.receiver.username,
            "body": "",
        }
        self.client.force_login(self.sender)
        response = self.client.post(self.list_create_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_message_by_empty_recipient_400_status(self):
        data = {
            "body": "test_post_message_by_empty_recipient_400_status",
        }
        self.client.force_login(self.sender)
        response = self.client.post(self.list_create_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_list_message_without_authentication_403_status(self):
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Detail Message (GET)
    def test_detail_message_200_status(self):
        # get API response
        self.client.force_login(self.sender)
        response = self.client.get(self.detail_url)
        # get data from db
        serializer = MessageModelSerializer(self.message)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_message_without_authentication_403_status(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
