import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string

from checks.utils import get_checks
from omcb import redis_connection


class CheckConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.redis_client = redis_connection.get_redis_client()

    async def connect(self):
        await self.accept()

        await self.channel_layer.group_add('global', self.channel_name)

        limit = redis_connection.CHECKS_BITSET_LIMIT
        checks = get_checks(self.redis_client, limit=limit, offset=0)
        count = self.redis_client.bitcount(redis_connection.CHECKS_BITSET_KEY)

        context = {
            'checks': checks,
            'count': count,
            'limit': limit,
            'offset': limit,
        }
        response = render_to_string('checks/initial_checks.html', context=context)

        await self.send(text_data=response)

    async def receive(self, text_data=None, bytes_data=None):
        assert text_data is not None

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
        context = {
            'status': event['status'],
            'origin': event['origin'],
            'count': event['count']
        }
        response = render_to_string('checks/update_checkbox.html', context=context)
        await self.send(text_data=response)
