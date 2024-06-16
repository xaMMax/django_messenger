from django import forms
from django.contrib.auth.models import User

from .models import Message, Chat, HiddenChat


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']


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
