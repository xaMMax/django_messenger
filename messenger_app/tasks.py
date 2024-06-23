import logging

from celery import shared_task
from messenger_app.models import Chat, UserProfile, Message

logger = logging.getLogger(__name__)


@shared_task
def print_chats_profiles():
    chats = Chat.objects.all()
    users = UserProfile.objects.all()
    for chat in chats:
        logger.info(f'Chats {chat.name}')
    for user in users:
        logger.info(f'User {user.user}')


@shared_task
def log_last_10_messages():
    messages = Message.objects.order_by('-created_at')[:10]
    logger.info("Logging the last 10 messages:")
    for message in messages:
        logger.info(f"{message.created_at}: {message.author.username} - {message.message}")
