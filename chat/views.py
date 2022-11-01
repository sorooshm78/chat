from django.views.generic import TemplateView
from django.contrib.auth.models import User

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import UserModelSerializer


# Create your views here.
class Home(TemplateView):
    template_name = 'core/chat.html'

class ListUser(ListAPIView):
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        current_user = self.request.user
        return User.objects.exclude(id=current_user.id)