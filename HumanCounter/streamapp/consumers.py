import json
from channels.generic.websocket import AsyncWebsocketConsumer

class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("stream_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("stream_group", self.channel_name)

    async def receive(self, text_data):
        pass  # We're not handling any incoming messages from WebSocket clients

    async def send_data(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))
