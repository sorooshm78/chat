import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from django.contrib.sessions.models import Session


class ChatConsumer(WebsocketConsumer):
    def get_user_id_from_sesstion(self, session_key):
        session = Session.objects.get(session_key=session_key)
        session_data = session.get_decoded()
        return session_data.get('_auth_user_id')

    def connect(self):
        session_key = str(self.scope['query_string']).split('=')[1][:-1]
        user_id = self.get_user_id_from_sesstion(session_key)
        self.user = f'user_{user_id}'

        async_to_sync(self.channel_layer.group_add)(
            self.user,
            self.channel_name,
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.user,
            self.channel_name,
        )

    def chat_message(self, event):
        message = event["message"]

        self.send(text_data=json.dumps({"type": "chat", "message": message}))
