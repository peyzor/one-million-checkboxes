from channels.generic.websocket import AsyncWebsocketConsumer


class MyTestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        print(text_data)

    async def disconnect(self, close_code):
        pass
