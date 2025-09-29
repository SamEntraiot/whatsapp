import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .models import Conversation, Message


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chat_list')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'chat/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST.get('email', '')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            login(request, user)
            return redirect('chat_list')
    return render(request, 'chat/register.html')


@login_required
def chat_list(request):
    conversations = Conversation.objects.filter(participants=request.user).order_by('-updated_at')
    # Get all users to start conversations with, excluding the current user
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/chat_list.html', {
        'conversations': conversations,
        'users': users,
        'current_user': request.user
    })


@login_required
def start_conversation(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        other_user = get_object_or_404(User, id=user_id)
        
        # Check if conversation already exists
        existing_conversation = Conversation.objects.filter(
            participants=request.user
        ).filter(participants=other_user).first()
        
        if existing_conversation:
            return redirect(f'/?chat={existing_conversation.id}')
        
        # Create new conversation
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)
        
        return redirect(f'/?chat={conversation.id}')
    
    return redirect('chat_list')


@login_required
def chat_room_content(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if not conversation.participants.filter(id=request.user.id).exists():
        return JsonResponse({'error': 'Not a participant'}, status=403)
    
    return render(request, 'chat/_chat_room_content.html', {
        'conversation': conversation,
        'current_user': request.user
    })


@login_required
def mark_messages_as_read(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message_ids = data.get('message_ids', [])
            conversation_id = data.get('conversation_id')

            if not conversation_id or not message_ids:
                return JsonResponse({'error': 'Missing data'}, status=400)

            # Update messages
            messages_to_update = Message.objects.filter(
                id__in=message_ids,
                conversation_id=conversation_id,
                is_read=False
            ).exclude(sender=request.user)
            
            updated_count = messages_to_update.update(is_read=True)

            # Notify via WebSocket
            if updated_count > 0:
                from channels.layers import get_channel_layer
                from asgiref.sync import async_to_sync
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f'chat_{conversation_id}',
                    {
                        'type': 'messages_read',
                        'sender_username': request.user.username,
                        'message_ids': message_ids
                    }
                )

            return JsonResponse({'status': 'success', 'updated_count': updated_count})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
def get_conversations(request):
    conversations = Conversation.objects.filter(participants=request.user).order_by('-updated_at')
    data = []
    for conv in conversations:
        last_message = conv.get_last_message()
        
        # Get the other participant for display
        other_participants = [p.username for p in conv.participants.all() if p != request.user]
        display_name = conv.get_display_name(request.user)
        avatar_initial = display_name[0].upper() if display_name else '?'
        
        data.append({
            'id': conv.id,
            'name': display_name,
            'avatar_initial': avatar_initial,
            'last_message': last_message.content if last_message else '',
            'last_message_time': last_message.timestamp.isoformat() if last_message else '',
            'participants': other_participants
        })
    return JsonResponse({'conversations': data})
