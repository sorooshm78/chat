from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import SessionAuthentication

from core import settings
from .serializers import UserModelSerializer, MessageModelSerializer
from .models import Message


# Create your views here.
class SessionCsrfExemptAuthentication(SessionAuthentication):
    """
    SessionAuthentication scheme used by DRF. DRF's SessionAuthentication uses
    Django's session framework for authentication which requires CSRF to be
    checked. In this case we are going to disable CSRF tokens for the API.
    """

    def enforce_csrf(self, request):
        return


class MessagePagination(PageNumberPagination):
    """
    Limit message prefetch to one page.
    """

    page_size = settings.MESSAGES_TO_LOAD


class Home(LoginRequiredMixin, TemplateView):
    template_name = "core/chat.html"


class ListUser(ListAPIView):
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        return User.objects.exclude(id=current_user.id)


class MessageModelViewSet(ModelViewSet):
    serializer_class = MessageModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionCsrfExemptAuthentication]
    queryset = Message.objects.all()
    allowed_methods = ["GET", "POST"]
    pagination_class = MessagePagination

    def list(self, request, *args, **kwargs):
        current_user = get_object_or_404(User, username=self.request.user)
        target = get_object_or_404(
            User, username=self.request.query_params.get("target")
        )
        self.queryset = self.queryset.filter(
            Q(user=current_user) | Q(user=target),
            Q(recipient=current_user) | Q(recipient=target),
        )

        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        current_user = get_object_or_404(User, username=self.request.user)
        self.queryset = self.queryset.filter(
            Q(user=current_user) | Q(recipient=current_user), Q(pk=kwargs["pk"])
        )

        return super().retrieve(request, *args, **kwargs)
