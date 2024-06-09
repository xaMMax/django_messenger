from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


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
    content = models.TextField()
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
        return f"{self.author.username}: {self.content[:20]}"
