from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http import HttpResponse
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from .serializers import UserSerializer

# Create your views here.
class Home(TemplateView):
    template_name = 'core/chat.html'

class Login(TemplateView):
    template_name = 'registration/login.html'

class Logout(View):
    def get(self, request):
        return HttpResponse('Logout User')


# api views
class ListUser(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MessageList(APIView):
    data = {}
    def get(self, request, *args, **kwargs):
        target = request.query_params.get('target')
        if target == 'sm':
            self.data = {
                'results' : [
                    {
                        'user' : 'sm',
                        'body' : 'personal message',
                        'timestamp' : 1667056856222,
                    },
                ]
            }
        else:
            self.data = {
                'results' : [
                    {
                        'user' : 'sm',
                        'body' : 'hi "a" user',
                        'timestamp' : 1807110465663,
                    },
                    {
                        'user' : 'a',
                        'body' : 'hi "sm" user',
                        'timestamp' : 1807110465663,
                    }
                ]
            }

        return Response(self.data)

    def post(self, request):
        return Response({'details':'send message ok'})


class MessageDetail(APIView):
    def get(self, request, id):
        date = {
            'results' : [
                {
                    'user' : 'sm',
                    'recipient' : 'a',
                    'body' : 'personal message',
                },
            ]
        }

        return Response(date)