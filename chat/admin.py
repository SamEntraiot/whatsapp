from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at']
    list_filter = ['created_at']
    filter_horizontal = ['participants']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'conversation', 'content', 'timestamp', 'is_read']
    list_filter = ['timestamp', 'is_read']
    search_fields = ['content', 'sender__username']
    readonly_fields = ['timestamp']
