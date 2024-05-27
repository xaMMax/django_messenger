from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Chat, Message
from .forms import MessageForm, ChatForm
from django.utils import timezone
from datetime import timedelta


@login_required
def chat_list(request):
    chats = Chat.objects.filter(users=request.user)
    return render(request, 'messenger/chat_list.html', {'chats': chats})


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user not in chat.users.all():
        return redirect('chat_list')

    messages = chat.messages.all()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.author = request.user
            message.save()
            return redirect('chat_detail', chat_id=chat.id)
    else:
        form = MessageForm()

    return render(request, 'messenger/chat_detail.html', {'chat': chat, 'messages': messages, 'form': form})


@permission_required('messenger.can_create_chat')
def create_chat(request):
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.save()
            chat.users.add(request.user)
            return redirect('chat_list')
    else:
        form = ChatForm()
    return render(request, 'messenger/create_chat.html', {'form': form})


@permission_required('messenger.can_add_users')
def add_user_to_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.method == 'POST':
        username = request.POST.get('username')
        user = get_object_or_404(User, username=username)
        chat.users.add(user)
        return redirect('chat_detail', chat_id=chat.id)
    return render(request, 'messenger/add_user.html', {'chat': chat})


@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user != message.author or timezone.now() - message.created_at > timedelta(days=1):
        return redirect('chat_detail', chat_id=message.chat.id)
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('chat_detail', chat_id=message.chat.id)
    else:
        form = MessageForm(instance=message)
    return render(request, 'messenger/edit_message.html', {'form': form, 'message': message})


@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user != message.author:
        return redirect('chat_detail', chat_id=message.chat.id)
    if request.method == 'POST':
        message.delete()
        return redirect('chat_detail', chat_id=message.chat.id)
    return render(request, 'messenger/delete_message.html', {'message': message})
