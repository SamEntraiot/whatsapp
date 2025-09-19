from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('chat/<int:conversation_id>/', views.chat_room, name='chat_room'),
    path('start-conversation/', views.start_conversation, name='start_conversation'),
    path('api/conversations/', views.get_conversations, name='get_conversations'),
    path('api/chat/<int:conversation_id>/', views.chat_room_content, name='chat_room_content'),
    path('api/messages/mark-as-read/', views.mark_messages_as_read, name='mark_messages_as_read'),
]
