from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Message

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class MessageModelSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    recipient = serializers.CharField(source='recipient.username')

    class Meta:
        model = Message
        fields = [
            'user',
            'recipient',
            'body',
            'timestamp',
        ]