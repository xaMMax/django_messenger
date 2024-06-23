from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatViewSet, MessageListCreateView, MessageRetrieveUpdateDestroyView

router = DefaultRouter()
router.register(r'chats', ChatViewSet, basename='chat')

urlpatterns = [
    path('', include(router.urls)),
    path('chats/<int:chat_id>/messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', MessageRetrieveUpdateDestroyView.as_view(), name='message-detail'),
]