from channels.generic.websocket import AsyncWebsocketConsumer
import json
from datetime import datetime
from .models import Profile, Message
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            await self.close()
        self.username = self.user.username
        self.group_name = self.username + str(self.user.id)
        await self.channel_layer.group_add(self.group_name,self.channel_name)
        await self.chat_groups_add()
        await self.accept()

    @database_sync_to_async
    def chat_groups_add(self):
        qs = Profile.objects.exclude(user__email=self.user.email)
        for p in qs:
            async_to_sync(self.channel_layer.group_add)((p.user.username+str(p.user.id)),self.channel_name)

    async def disconnect(self,close_code):
        #await self.channel_layer.group_discard(self.group_chat_name, self.channel_name)
        await self.channel_layer.group_send(self.group_name, ({
                'type':'on.connect',
                'disconnected_user':self.username,
        }))
        await self.close()

    async def receive(self,text_data):
        text_data_obj = json.loads(text_data)
        delete = text_data_obj.get('delete',None)
        if delete:
            self.selected_messages = text_data_obj['selected_messages']
            await self.delete_message()
            self.receiver = text_data_obj['receiver']
            self.sender = text_data_obj['sender']
            recv_user_log = await self.get_chat_receiver()
            await self.channel_layer.group_send(self.group_name,({
                    'type':'chat.delete',
                    "sender": self.username,
                    "selected_messages":self.selected_messages,
                    "receiver":self.receiver,
                    'recv_user_log':recv_user_log
            }))
        else:
            self.message = text_data_obj['message']
            self.receiver = text_data_obj['receiver']
            receiver_log = text_data_obj['receiver_log']
            self.sender = text_data_obj['sender']
            recv_user_log = await self.get_chat_receiver()
            msg_obj = await self.create_message()
            text = msg_obj.text
            timestamp = msg_obj.created.strftime("%Y-%m-%d, %H:%M")
            await self.channel_layer.group_send(self.group_name,({
                    'type':'chat.send',
                    "sender": self.username,
                    "message":text,
                    "timestamp": timestamp,
                    "receiver":self.receiver,
                    'receiver_log':receiver_log,
                    'recv_user_log':recv_user_log
            }))

    @database_sync_to_async
    def create_message(self):
        return Message.objects.create(user=self.user,text=self.message,receiver=self.receiver)

    @database_sync_to_async
    def delete_message(self):
        for id in self.selected_messages:
            Message.objects.get(pk=id).delete()
            print('message with id', id,'deleted')
    
    @database_sync_to_async
    def get_chat_receiver(self):
        receiving_user = User.objects.get(username=self.sender)
        return 'chat' + str(receiving_user.id) + receiving_user.username

    async def chat_send(self,event):
        message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']
        receiver = event['receiver']
        receiver_log = event['receiver_log']
        recv_user_log = event['recv_user_log']
        await self.send(text_data = json.dumps({
            'message':message,
            'timestamp':timestamp,
            'sender':sender,
            'receiver':receiver,
            'receiver_log':receiver_log,
            'recv_user_log':recv_user_log
            })
        )

    async def chat_delete(self,event):
        selected_messages = event['selected_messages']
        sender = event['sender']
        receiver = event['receiver']
        recv_user_log = event['recv_user_log']
        await self.send(text_data = json.dumps({
            'message_delete':True,
            'selected_messages':selected_messages,
            'sender':sender,
            'receiver':receiver,
            'recv_user_log':recv_user_log
            })
        )

    async def on_connect(self,event):
        connected_user = event.get('connected_user',None)
        disconnected_user = event.get('disconnected_user',None)
        if connected_user:
            await self.send(text_data= json.dumps({
            'connected_user':connected_user
            }))
        else:
            await self.send(text_data= json.dumps({
            'disconnected_user':disconnected_user
            }))
        
        
       
        