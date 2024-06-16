from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model, user_logged_in, user_logged_out
from django.utils import timezone

from messenger.models import ActivityLog, UserProfile

User = get_user_model()


@receiver(post_save, sender=User)
def log_user_activity(sender, instance, created, **kwargs):
    action = "User is created" if created else "updated user data"
    ActivityLog.objects.create(user=instance, action=action)


@receiver(pre_save, sender=User)
def log_user_activity_pre(sender, instance, **kwargs):
    default_email = instance.email or f"{instance.username}.nonreal@fakemail.com"
    action = f"Set default email to {default_email} for user {instance.username}" if not instance.email else False
    instance.email = instance.email or default_email
    if action:
        ActivityLog.objects.create(action=default_email)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

