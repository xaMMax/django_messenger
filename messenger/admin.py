from django.contrib import admin, messages
from django.contrib.auth.models import User

from messenger.models import Message, Chat, HiddenChat, ForgottenPasswordRequest, ActivityLog, PrivateMessage, \
    UserProfile


# Register your models here.


class ChatAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'hidden')
    fields = ('name', 'users', 'hidden')
    readonly_fields = ('created_at',)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'author', 'message', 'created_at', 'updated_at')
    fields = ('chat', 'author', 'message', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'created_at')
    fields = ('sender', 'recipient', 'content')

    def response_add(self, request, obj, post_url_continue=None):
        response = super().response_add(request, obj, post_url_continue)
        if obj.recipient.is_superuser:
            self.message_user(request, f'Message "{obj}" to superuser has been sent successfully!', messages.SUCCESS)
        else:
            self.message_user(request, f'Message "{obj}" has been sent successfully!', messages.SUCCESS)
        return response


admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(HiddenChat)
admin.site.register(ForgottenPasswordRequest)
admin.site.register(ActivityLog)
admin.site.register(PrivateMessage, PrivateMessageAdmin)
admin.site.register(UserProfile)
