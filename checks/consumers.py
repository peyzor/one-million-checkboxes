import json

from channels.generic.websocket import AsyncWebsocketConsumer


class CheckConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        await self.channel_layer.group_add('global', self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        status = int(text_data_json.get('status', 0))
        origin = text_data_json['HEADERS']['HX-Trigger']

        await self.channel_layer.group_send(
            'global',
            {
                'type': 'update.checkbox',
                'status': status,
                'origin': origin
            }
        )

    async def update_checkbox(self, event):
        status = event['status']
        origin = event['origin']

        response = f"""
            <input type="checkbox" id="{origin}" name="status" value={1 - status} {"checked" if status else ""} ws-send>
        """
        await self.send(text_data=response)
