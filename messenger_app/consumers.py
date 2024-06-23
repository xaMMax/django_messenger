import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat, Message
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'

        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = self.scope["user"]

        chat = await sync_to_async(Chat.objects.get)(id=self.chat_id)
        message = await sync_to_async(Message.objects.create)(
            chat=chat,
            author=user,
            message=message
        )

        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message.message,
                'author': message.author.username,
                'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        )

    async def chat_message(self, event):
        message = event['message']
        author = event['author']
        created_at = event['created_at']

        await self.send(text_data=json.dumps({
            'message': message,
            'author': author,
            'created_at': created_at
        }))
