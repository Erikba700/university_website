import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage, ChatRoom


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']

        message_id = await self.save_message(user, message)

        await self.send_chat_message(message, message_id)

    async def send_chat_message(self, message, message_id):
        await self.send(text_data=json.dumps({
            'message': message,
            'message_id': message_id,
            'timestamp': self.get_timestamp(),
            'user': self.scope['user'].username
        }))

    @database_sync_to_async
    def save_message(self, user, message):
        chat_room = ChatRoom.objects.get(name=self.room_name)
        chat_message = ChatMessage.objects.create(user=user, text=message, room=chat_room)
        return chat_message.id

    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
