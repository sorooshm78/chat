import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    
    def connect(self):
        self.session_id = 'test-session'

        async_to_sync(self.channel_layer.group_add)(
            self.session_id,
            self.channel_name,
        )

        self.accept()
      
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.session_id,
            self.channel_name,
        )
    
    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))