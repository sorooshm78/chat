from operator import imod
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from .models import Message

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class MessageModelSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='sender.username', read_only=True)
    recipient = serializers.CharField(source='receiver.username')

    def create(self, validated_data):
        sender = self.context['request'].user
        receiver = get_object_or_404(User, username=validated_data['receiver']['username'])
    
        print(f'{sender} -> {receiver}')

        return Message.objects.create(
            sender=sender,
            receiver=receiver,
            body=validated_data['body'], 
            timestamp=125, 
        )

    class Meta:
        model = Message
        fields = [
            'user',
            'recipient',
            'body',
            'timestamp',
        ]
        read_only_fields = [
            'user',
            'timestamp',
        ]