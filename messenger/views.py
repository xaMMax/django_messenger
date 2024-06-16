from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction, IntegrityError
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, FormView, TemplateView, CreateView
from rest_framework import generics

from .mixins import ChatListMixin, ChatDetailMixin, CreateChatMixin, AddUserToChatMixin, EditMessageMixin, \
    DeleteMessageMixin, UpdateTimestampMixin, JSONResponseMixin, AdminRequiredMixin, \
    FormInitialDataMixin, ProfileOwnerRequiredMixin, SuperuserRequiredMixin
from .models import Chat, Message, HiddenChat, PrivateMessage, UserProfile
from .forms import MessageForm, UserRegisterForm, ForgotPasswordForm, PrivateMessageForm, ChatForm
from django.contrib.auth import get_user_model

from .serializers import UserProfileSerializer

User = get_user_model()


class ForgotPasswordView(FormInitialDataMixin, FormView):
    template_name = 'registration/forgot_password.html'
    form_class = ForgotPasswordForm
    success_url = '/'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        try:
            user = User.objects.filter(email=email).first()
            if user:
                forgot_password_request = form.save(commit=False)
                forgot_password_request.user = user
                forgot_password_request.save()
            messages.info(self.request, 'Your message has been sent to the administrator.')
            return redirect('login')

        except PermissionDenied as e:
            messages.error(self.request, str(e))


class NewLoginView(FormInitialDataMixin, LoginView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        messages.success(request, 'Welcome to Messenger!')
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You are now logged in!')
            return redirect('chat_list')
        elif not form.is_valid():
            messages.error(request, 'Invalid username or password.')
            return render(request, self.template_name, {'form': form})


class RegistrationView(View):
    template_name = 'registration/register.html'
    form_class = UserRegisterForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            messages.success(request, 'Account was successfully created.')
            return redirect('login')
        return render(request, self.template_name, {'form': form})


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
        context['messages'] = self.get_object().messages.all()
        context['form'] = MessageForm()
        chat_users = self.get_object().users.all()
        context['users'] = chat_users
        chat_user_profiles = UserProfile.objects.filter(user__in=chat_users)
        online_threshold = timezone.now() - timedelta(minutes=5)
        context['online_users'] = [profile for profile in chat_user_profiles if profile.is_online()]
        context['offline_users'] = [profile for profile in chat_user_profiles if not profile.is_online()]

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


class CreateChatView(LoginRequiredMixin, FormInitialDataMixin, CreateChatMixin, CreateView):
    model = Chat
    form_class = ChatForm
    success_url = reverse_lazy('chat_list')
    initial_data = {'name': 'Default Chat Name'}

    def form_valid(self, form):
        response = super().form_valid(form)
        chat_name = form.instance.name
        messages.success(self.request, f'Chat "{chat_name}" successfully created!')
        return response


class DeleteChatView(LoginRequiredMixin, SuperuserRequiredMixin, DeleteView):
    model = Chat
    success_url = reverse_lazy('chat_list')
    template_name = 'messenger/chat_confirm_delete.html'


class AddUserToChatView(LoginRequiredMixin, AddUserToChatMixin):
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


class ChatMessagesJSONView(LoginRequiredMixin, AdminRequiredMixin, JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        chat_id = kwargs.get('pk')
        chat = Chat.objects.get(pk=chat_id)
        messages_all = chat.messages.all()
        data = {
            'messages': [
                {
                    'chat_name': message.chat.name,
                    'author': message.author.username,
                    'message': message.message,
                    'created_at': message.created_at,
                    'updated_at': message.updated_at,
                } for message in messages_all
            ]
        }
        return self.render_to_json_response(data)


class UserProfileView(LoginRequiredMixin, DetailView, FormView):
    model = User
    template_name = 'messenger/user_profile.html'
    context_object_name = 'user_profile'
    form_class = PrivateMessageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        if self.request.user == self.get_object():
            context['received_messages'] = PrivateMessage.objects.filter(recipient=self.get_object())
            context['sent_messages'] = PrivateMessage.objects.filter(sender=self.get_object())
        else:
            context['received_messages'] = []
            context['sent_messages'] = PrivateMessage.objects.filter(sender=self.get_object())

        # Отримання списку користувачів і перевірка їх статусу онлайн
        now = timezone.now()
        online_users = []
        offline_users = []

        for user in User.objects.all():
            last_activity = user.userprofile.last_activity
            if last_activity and (now - last_activity) < timedelta(minutes=5):
                online_users.append(user)
            else:
                offline_users.append(user)

        context['online_users'] = online_users
        context['offline_users'] = offline_users

        return context

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.save()
        messages.success(self.request, 'Your message has been sent.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'pk': self.kwargs['pk']})

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error with your submission. Please try again.')
        return super().form_invalid(form)


class UserStatusList(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


