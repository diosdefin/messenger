from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Message

class MessageInline(admin.TabularInline):
    model = Message
    fk_name = 'sender'
    extra = 0

class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'date_joined', 'is_staff', 'is_active']
    list_editable = ['is_active']
    inlines = [MessageInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'content_short', 'timestamp', 'is_read']
    list_filter = ['sender', 'receiver', 'timestamp']
    list_editable = ['is_read']

    def content_short(self, obj):
        return obj.content[:50]
    content_short.short_description = 'Сообщение'