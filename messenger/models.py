import datetime
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_activity = models.DateTimeField(default=timezone.now)

    def is_online(self):
        now = timezone.now()
        return (now - self.last_activity) < timedelta(minutes=5)

    def __str__(self):
        return self.user.username


class Chat(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class HiddenChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.chat.name}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        permissions = [
            ("can_create_chat", "Can create chat"),
            ("can_add_users", "Can add users to chat"),
            ("can_remove_users", "Can remove users from chat"),
            ("can_edit_message", "Can edit message"),
            ("can_delete_message", "Can delete message"),
        ]
        # fields = ['chat', 'author', 'content', 'created_at', 'updated_at']

    def __str__(self):
        return f"{self.author.username}: {self.message[:20]}"


class ForgottenPasswordRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset request from {self.email} at {self.created_at}"


class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    action = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Someone'}: {self.action}"


class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username}: {self.content[:20]}"

