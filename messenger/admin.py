from django.contrib import admin
from django.contrib.auth.models import User

from messenger.models import Message, Chat, HiddenChat


# Register your models here.


class ChatAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'hidden')
    fields = ('name', 'users', 'hidden')
    readonly_fields = ('created_at',)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'author', 'content', 'created_at', 'updated_at')
    fields = ('chat', 'author', 'content', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(HiddenChat)

