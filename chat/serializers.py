from time import time

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from .models import Message


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class MessageModelSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    recipient = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    def create(self, validated_data):
        ModelClass = self.Meta.model
        sender = self.context['request'].user
        receiver = get_object_or_404(User, username=validated_data['recipient'])

        return ModelClass.objects.create(
            user=sender,
            recipient=receiver,
            body=validated_data['body'], 
            timestamp=int(time()*1000), 
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
            'timestamp',
        ]