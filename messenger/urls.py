from django.urls import path
from .views import ChatListView, ChatDetailView, CreateChatView, AddUserToChatView, EditMessageView, DeleteMessageView, \
    ChatMessagesJSONView, hide_chat, unhide_chat, HiddenChatListView, UserProfileView, \
    UserStatusList, DeleteChatView

urlpatterns = [
    path('', ChatListView.as_view(), name='chat_list'),
    path('hidden_chats/', HiddenChatListView.as_view(), name='hidden_chats'),
    path('chat/<int:pk>/', ChatDetailView.as_view(), name='chat_detail'),
    path('chat/create/', CreateChatView.as_view(), name='create_chat'),
    path('chat/<int:pk>/add_user/', AddUserToChatView.as_view(), name='add_user_to_chat'),
    path('message/<int:message_id>/edit/', EditMessageView.as_view(), name='edit_message'),
    path('message/<int:message_id>/delete/', DeleteMessageView.as_view(), name='delete_message'),
    path('chat/<int:pk>/json/', ChatMessagesJSONView.as_view(), name='chat_messages_json'),
    path('chat/<int:chat_id>/hide/', hide_chat, name='hide_chat'),
    path('chat/<int:chat_id>/unhide/', unhide_chat, name='unhide_chat'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
    path('api/update-last-activity/', UserStatusList.as_view(), name='update_last_activity'),
    path('chat/<int:pk>/delete/', DeleteChatView.as_view(), name='delete_chat'),

]
