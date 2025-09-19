from django.test import TestCase
from django.contrib.auth.models import User
from .models import Conversation, Message


class ConversationModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass')
        self.user2 = User.objects.create_user(username='user2', password='testpass')
    
    def test_direct_conversation_creation(self):
        conversation = Conversation.objects.create(conversation_type='direct')
        conversation.participants.add(self.user1, self.user2)
        
        self.assertEqual(conversation.conversation_type, 'direct')
        self.assertEqual(conversation.participants.count(), 2)
        self.assertIn(self.user1, conversation.participants.all())
        self.assertIn(self.user2, conversation.participants.all())
    
    def test_group_conversation_creation(self):
        conversation = Conversation.objects.create(
            name='Test Group',
            conversation_type='group'
        )
        conversation.participants.add(self.user1, self.user2)
        
        self.assertEqual(conversation.name, 'Test Group')
        self.assertEqual(conversation.conversation_type, 'group')
        self.assertEqual(str(conversation), 'Test Group')


class MessageModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass')
        self.user2 = User.objects.create_user(username='user2', password='testpass')
        self.conversation = Conversation.objects.create(conversation_type='direct')
        self.conversation.participants.add(self.user1, self.user2)
    
    def test_message_creation(self):
        message = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            content='Hello, World!'
        )
        
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.content, 'Hello, World!')
        self.assertEqual(message.conversation, self.conversation)
        self.assertFalse(message.is_read)
    
    def test_message_to_dict(self):
        message = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            content='Test message'
        )
        
        message_dict = message.to_dict()
        
        self.assertEqual(message_dict['sender'], 'user1')
        self.assertEqual(message_dict['content'], 'Test message')
        self.assertFalse(message_dict['is_read'])
