from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import UserModelSerializer, MessageModelSerializer
from .models import Message


# Create your views here.
class Home(TemplateView):
    template_name = 'core/chat.html'


class ListUser(ListAPIView):
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        current_user = self.request.user
        return User.objects.exclude(id=current_user.id)


class ListCreateMessage(ListCreateAPIView):
    serializer_class = MessageModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user = get_object_or_404(User, username=self.request.user)
        target = get_object_or_404(User, username=self.request.query_params.get('target'))

        return Message.objects.filter(
            Q(sender=current_user) | Q(sender=target),
            Q(receiver=current_user) | Q(receiver=target)
        )

    def filter_queryset(self, queryset):
        return queryset.order_by(
            '-timestamp'
        )

    def list(self, request, *args, **kwargs):
        message_list = super().list(request, *args, **kwargs).data
        return Response({
            'results' : message_list,
        })
