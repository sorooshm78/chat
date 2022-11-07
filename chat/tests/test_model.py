from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Message


class TestModelMessage(TestCase):
    def setUp(self):
        self.sender = User.objects.create(username="sender", password="a/@1234567")
        self.receiver = User.objects.create(username="receiver", password="a/@1234567")

    def test_string_representation(self):
        message = Message.objects.create(
            user=self.sender,
            recipient=self.receiver,
            body="test_string_representation",
        )
        self.assertEqual(str(message), f"{self.sender} -> {self.receiver}")

    def test_create_message_with_valid_data(self):
        message = Message.objects.create(
            user=self.sender,
            recipient=self.receiver,
            body="test_create_message_with_valid_data",
        )

        self.assertTrue(Message.objects.filter(pk=message.id).exists())
        self.assertEqual(message.body, "test_create_message_with_valid_data")

    def test_create_message_without_sender(self):
        with self.assertRaises(AttributeError):
            Message.objects.create(
                recipient=self.receiver,
                body="test_create_message_without_sender",
            )

    def test_create_message_without_receiver(self):
        with self.assertRaises(AttributeError):
            Message.objects.create(
                user=self.sender,
                body="test_create_message_without_receiver",
            )
