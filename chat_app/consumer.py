# from django.contrib.auth import authenticate
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from chat_app.models import *
import json


class MyConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["group_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
    

        await self.accept()
        print("websocket connected........")




    # Receive message from WebSocket
    async def receive(self, text_data):

        data = json.loads(text_data)
        msg = data['msg']

        
        group = await Group.objects.aget(name = self.room_name)

        if self.scope['user'].is_authenticated:
            chat = Chat(content = msg, group = group)
            await database_sync_to_async(chat.save)()

            scope_user =self.scope['user'].username
            data['user'] = scope_user

            await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": json.dumps(data)}
                )

        else:
            self.send({
                'text':json.dumps({"msg":"Login Required"})
            })

        

    # Receive message from room group
    async def chat_message(self, event):
        print("message from server.....",event)
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data= message)
        


async def disconnect(self, close_code):

        print("websocket dicconnected.....",close_code)
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)