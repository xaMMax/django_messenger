from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from .mixins import ChatListMixin, ChatDetailMixin, CreateChatMixin, AddUserToChatMixin, EditMessageMixin, \
    DeleteMessageMixin, UpdateTimestampMixin, JSONResponseMixin, SuccessMessageMixin, AdminRequiredMixin, \
    FormInitialDataMixin
from .models import Chat, Message, HiddenChat
from .forms import MessageForm


class ChatListView(ChatListMixin, ListView):
    model = Chat
    template_name = 'messenger/chat_list.html'
    context_object_name = 'chats'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hidden_chats'] = HiddenChat.objects.filter(user=self.request.user).select_related('chat')
        return context

    def get_queryset(self):
        return self.get_chats()


class HiddenChatListView(ChatListMixin, ListView):
    model = Chat
    template_name = 'messenger/hidden_chats.html'
    context_object_name = 'chats'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hidden_chats'] = HiddenChat.objects.filter(user=self.request.user).select_related('chat')
        return context

    def get_queryset(self):
        return self.get_chats()


@login_required
def hide_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    chat.hidden = True
    chat.save()
    HiddenChat.objects.get_or_create(user=request.user, chat=chat, hidden=True)
    return redirect('chat_list')


@login_required
def unhide_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    chat.hidden = False
    chat.save()
    HiddenChat.objects.filter(user=request.user, chat=chat).delete()
    return redirect('chat_list')


class ChatDetailView(ChatDetailMixin, DetailView):
    model = Chat
    template_name = 'messenger/chat_detail.html'
    context_object_name = 'chat'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = self.chat.messages.all()
        context['form'] = MessageForm()
        context['users'] = self.chat.users.all()
        return context

    def post(self, request, *args, **kwargs):
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = self.chat
            message.author = request.user
            message.save()
            return redirect('chat_detail', pk=self.chat.pk)
        return self.get(request, *args, **kwargs)


class CreateChatView(FormInitialDataMixin, CreateChatMixin, ):
    success_message = "Chat created successfully"
    success_url = reverse_lazy('chat_list')
    initial_data = {'name': 'Default Chat Name'}


class AddUserToChatView(AddUserToChatMixin):
    success_url = reverse_lazy('chat_detail')


class EditMessageView(UpdateTimestampMixin, EditMessageMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'messenger/edit_message.html'
    pk_url_kwarg = 'message_id'

    def get_success_url(self):
        return reverse_lazy('chat_detail', kwargs={'pk': self.message.chat.pk})


class DeleteMessageView(DeleteMessageMixin, DeleteView):
    model = Message
    template_name = 'messenger/delete_message.html'
    pk_url_kwarg = 'message_id'

    def get_success_url(self):
        return reverse_lazy('chat_detail', kwargs={'pk': self.message.chat.pk})


class ChatMessagesJSONView(AdminRequiredMixin, JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        chat_id = kwargs.get('pk')
        chat = Chat.objects.get(pk=chat_id)
        messages = chat.messages.all()
        data = {
            'messages': [
                {
                    'chat_name': message.chat.name,
                    'author': message.author.username,
                    'content': message.content,
                    'created_at': message.created_at,
                    'updated_at': message.updated_at,
                } for message in messages
            ]
        }
        return self.render_to_json_response(data)
