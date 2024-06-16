from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    is_online = serializers.BooleanField()

    class Meta:
        model = UserProfile
        fields = ['user', 'is_online']
