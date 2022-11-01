from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='receiver')
    body = models.CharField(max_length=250)
    timestamp = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.sender} -> {self.receiver}'
