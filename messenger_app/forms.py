from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Message, Chat, HiddenChat, ForgottenPasswordRequest, PrivateMessage


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'send_message_form', 'cols': 80, 'rows': 3}),
        }


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['name']


class AddUserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Select User")


class HiddenChatForm(forms.ModelForm):
    class Meta:
        model = HiddenChat
        fields = ['chat']


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ForgotPasswordForm(forms.ModelForm):
    class Meta:
        model = ForgottenPasswordRequest
        fields = ['email', 'message']


class PrivateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['content', 'recipient']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
        }
