import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string

from checks.utils import get_initial_state
from omcb import redis_connection


class CheckConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.redis_client = redis_connection.get_redis_client()

    async def connect(self):
        await self.accept()

        await self.channel_layer.group_add('global', self.channel_name)

        initial_state = get_initial_state(self.redis_client)
        response = render_to_string('checks/initial_state.html', context=initial_state)

        await self.send(text_data=response)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        status = int(text_data_json.get('status', 0))
        origin = text_data_json['HEADERS']['HX-Trigger']

        offset = int(origin.split('-')[-1])
        self.redis_client.setbit(redis_connection.CHECKS_BITSET_KEY, offset, status)

        count = self.redis_client.bitcount(redis_connection.CHECKS_BITSET_KEY)

        await self.channel_layer.group_send(
            'global',
            {
                'type': 'update.checkbox',
                'status': status,
                'origin': origin,
                'count': count
            }
        )

    async def update_checkbox(self, event):
        status = event['status']
        origin = event['origin']
        count = event['count']

        response = f"""
            <p id="count" hx-swap-oob="true">{count}</p>
            <input type="checkbox" id="{origin}" name="status" value={1 - status} {"checked" if status else ""} ws-send>
        """
        await self.send(text_data=response)
