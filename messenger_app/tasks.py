from celery import shared_task


@shared_task
def update_all_chats():
    # ваш код завдання
    from messenger_app.models import Chat
    print(Chat.objects.all())
    from messenger_app.models import UserProfile
    print(UserProfile.objects.all())
