from asgiref.sync import async_to_sync

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from channels.layers import get_channel_layer


# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="sender"
    )
    recipient = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="receiver"
    )
    body = models.CharField(max_length=250)
    timestamp = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.user} -> {self.recipient}"


@receiver(post_save, sender=Message)
def notifies_users(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "test-session", {"type": "chat_message", "message": instance.id}
    )
