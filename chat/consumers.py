import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Conversation, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.conversation_group_name = f'chat_{self.conversation_id}'
        
        # Join conversation group
        await self.channel_layer.group_add(
            self.conversation_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send recent messages when user connects
        messages = await self.get_recent_messages()
        await self.send(text_data=json.dumps({
            'type': 'recent_messages',
            'messages': messages
        }))

    async def disconnect(self, close_code):
        # Leave conversation group
        await self.channel_layer.group_discard(
            self.conversation_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type', 'chat_message')
            
            if message_type == 'chat_message':
                message = text_data_json['message']
                username = text_data_json['username']
                
                # Save message to database
                saved_message = await self.save_message(username, message)
                
                if saved_message:
                    # Send message to conversation group
                    await self.channel_layer.group_send(
                        self.conversation_group_name,
                        {
                            'type': 'chat_message',
                            'message': saved_message
                        }
                    )
            elif message_type == 'typing':
                username = text_data_json['username']
                is_typing = text_data_json['is_typing']
                
                # Broadcast typing status to group
                await self.channel_layer.group_send(
                    self.conversation_group_name,
                    {
                        'type': 'typing_status',
                        'username': username,
                        'is_typing': is_typing
                    }
                )
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'Error processing message: {str(e)}'
            }))

    async def chat_message(self, event):
        message = event['message']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message
        }))

    async def messages_read(self, event):
        # Broadcast the read status to other users in the group
        await self.send(text_data=json.dumps({
            'type': 'messages_read',
            'message_ids': event['message_ids'],
            'sender_username': event['sender_username']
        }))

    async def typing_status(self, event):
        # Send typing status to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'typing_status',
            'username': event['username'],
            'is_typing': event['is_typing']
        }))

    @database_sync_to_async
    def save_message(self, username, message):
        try:
            user = User.objects.get(username=username)
            conversation = Conversation.objects.get(id=self.conversation_id)
            
            # Check if user is a participant in the conversation
            if not conversation.participants.filter(id=user.id).exists():
                return None
            
            message_obj = Message.objects.create(
                conversation=conversation,
                sender=user,
                content=message
            )
            
            # Update conversation timestamp
            conversation.save()
            
            return message_obj.to_dict()
        except (User.DoesNotExist, Conversation.DoesNotExist):
            return None

    @database_sync_to_async
    def get_recent_messages(self):
        try:
            conversation = Conversation.objects.get(id=self.conversation_id)
            messages = conversation.messages.order_by('-timestamp')[:50]
            return [msg.to_dict() for msg in reversed(messages)]
        except Conversation.DoesNotExist:
            return []
