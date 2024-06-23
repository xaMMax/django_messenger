from rest_framework import serializers
from messenger_app.models import Chat, Message
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ChatSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'name', 'users', 'created_at', 'hidden']


class MessageSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    chat = serializers.PrimaryKeyRelatedField(queryset=Chat.objects.all())

    class Meta:
        model = Message
        fields = ['id', 'chat', 'author', 'message', 'created_at', 'updated_at']