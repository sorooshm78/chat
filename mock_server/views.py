from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http import HttpResponse

# Create your views here.
class Home(TemplateView):
    template_name = 'core/chat.html'

class Login(TemplateView):
    template_name = 'registration/login.html'

class Logout(View):
    def get(self, request):
        return HttpResponse('Logout User')


# api views
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from .serializers import UserSerializer

class ListUser(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer