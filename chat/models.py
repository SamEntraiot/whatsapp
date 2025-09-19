from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        participants = list(self.participants.all())
        if len(participants) >= 2:
            return f"{participants[0].username} & {participants[1].username}"
        elif len(participants) == 1:
            return f"{participants[0].username}"
        return f"Conversation {self.id}"
    
    def get_display_name(self, current_user):
        """Get conversation name for display to a specific user"""
        participants = list(self.participants.all())
        # For direct messages, show the other participant's name
        for participant in participants:
            if participant != current_user:
                return participant.username
        # If only current user (shouldn't happen), show their name
        return current_user.username if participants else "Unknown"
    
    def get_last_message(self):
        return self.messages.order_by('-timestamp').first()


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}..."
    
    def to_dict(self):
        return {
            'id': self.id,
            'sender': self.sender.username,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'is_read': self.is_read,
        }
