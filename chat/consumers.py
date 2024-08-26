import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            'test',
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            'test',
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']

        response = f"""
            <ul hx-swap-oob="beforeend:#notifications"><li class="message">{message}</li></ul>
        """
        self.send(text_data=response)
