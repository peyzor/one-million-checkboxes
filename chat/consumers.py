import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        await self.channel_layer.group_add('test', self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            'test',
            {
                'type': 'chat.message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        response = f"""
            <ul hx-swap-oob="beforeend:#notifications"><li class="message">{message}</li></ul>
        """
        await self.send(text_data=response)
