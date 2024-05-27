from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list, name='chat_list'),  # Основний шлях для кореневого URL
    path('chat/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('chat/create/', views.create_chat, name='create_chat'),
    path('chat/<int:chat_id>/add_user/', views.add_user_to_chat, name='add_user_to_chat'),
    path('message/<int:message_id>/edit/', views.edit_message, name='edit_message'),
    path('message/<int:message_id>/delete/', views.delete_message, name='delete_message'),
]
