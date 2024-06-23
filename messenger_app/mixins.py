from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

from django.views.generic import ListView, CreateView, FormView

from messenger_app.forms import ChatForm, AddUserForm
from messenger_app.models import Chat, Message, HiddenChat


class ChatListMixin(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def get_chats(self):
        user = self.request.user
        hidden_chats = HiddenChat.objects.filter(user=user).values_list('chat', flat=True)
        return user.chats.exclude(id__in=hidden_chats)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chats'] = Chat.objects.filter(users=self.request.user)
        return context


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class ChatDetailMixin(LoginRequiredMixin):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        self.chat = get_object_or_404(Chat, id=kwargs['pk'])
        if request.user not in self.chat.users.all():
            return redirect('chat_list')
        return super().dispatch(request, *args, **kwargs)


class CreateChatMixin(PermissionRequiredMixin, CreateView):
    permission_required = 'messenger_app.can_create_chat'
    template_name = 'messenger_app/create_chat.html'
    form_class = ChatForm

    def form_valid(self, form):
        chat = form.save()
        chat.users.add(self.request.user)
        return redirect('chat_list')


class AddUserToChatMixin(PermissionRequiredMixin, FormView):
    permission_required = 'messenger_app.can_add_users'
    template_name = 'messenger_app/add_user.html'
    form_class = AddUserForm

    def dispatch(self, request, *args, **kwargs):
        self.chat = get_object_or_404(Chat, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.cleaned_data['user']
        self.chat.users.add(user)
        return redirect('chat_detail', pk=self.chat.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chat'] = self.chat
        return context


class EditMessageMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        self.message = get_object_or_404(Message, id=kwargs['message_id'])
        if request.user != self.message.author or timezone.now() - self.message.created_at > timedelta(days=1):
            return redirect('chat_detail', pk=self.message.chat.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = self.message
        return context

    def form_valid(self, form):
        form.instance.updated_at = timezone.now()
        return super().form_valid(form)


class DeleteMessageMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        self.message = get_object_or_404(Message, id=kwargs['message_id'])
        if request.user != self.message.author:
            return redirect('chat_detail', pk=self.message.chat.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = self.message
        return context

    def post(self, request, *args, **kwargs):
        self.message.delete()
        return redirect('chat_detail', pk=self.message.chat.pk)


class UpdateTimestampMixin:
    def form_valid(self, form):
        form.instance.updated_at = timezone.now()
        return super().form_valid(form)


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return PermissionDenied("You do not have permission to view this page.")


class JSONResponseMixin:
    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(self.get_data(context), **response_kwargs)

    def get_data(self, context):
        return context


class FormInitialDataMixin:
    initial_data = {}

    def get_initial(self):
        initial = super().get_initial()
        initial.update(self.initial_data)
        return initial


class ProfileOwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.get_object() != request.user:
            raise PermissionDenied("You do not have permission to view this profile.")
        return super().dispatch(request, *args, **kwargs)
