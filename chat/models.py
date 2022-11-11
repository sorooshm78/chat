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
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user} -> {self.recipient}"

    class Meta:
        ordering = ("-timestamp",)


@receiver(post_save, sender=Message)
def notifies_users(sender, instance, **kwargs):
    user_id = str(instance.user.id)
    recipient_id = str(instance.recipient.id)

    notification = {"type": "chat_message", "message": f"{instance.id}"}

    channel_layer = get_channel_layer()
    # send message to sender
    async_to_sync(channel_layer.group_send)(user_id, notification)
    # send message to receiver
    async_to_sync(channel_layer.group_send)(recipient_id, notification)
