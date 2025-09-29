from django.test import TestCase
from django.contrib.auth.models import User
from .models import Conversation, Message


class ConversationModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass')
        self.user2 = User.objects.create_user(username='user2', password='testpass')
    
    def test_conversation_creation(self):
        conversation = Conversation.objects.create()
        conversation.participants.add(self.user1, self.user2)
        
        self.assertEqual(conversation.participants.count(), 2)
        self.assertIn(self.user1, conversation.participants.all())
        self.assertIn(self.user2, conversation.participants.all())
    
    def test_conversation_display_name(self):
        conversation = Conversation.objects.create()
        conversation.participants.add(self.user1, self.user2)
        
        # Test display name for user1 (should show user2's name)
        display_name = conversation.get_display_name(self.user1)
        self.assertEqual(display_name, 'user2')
        
        # Test display name for user2 (should show user1's name)
        display_name = conversation.get_display_name(self.user2)
        self.assertEqual(display_name, 'user1')
    
    def test_conversation_str_representation(self):
        conversation = Conversation.objects.create()
        conversation.participants.add(self.user1, self.user2)
        
        str_repr = str(conversation)
        self.assertIn('user1', str_repr)
        self.assertIn('user2', str_repr)


class MessageModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass')
        self.user2 = User.objects.create_user(username='user2', password='testpass')
        self.conversation = Conversation.objects.create()
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
