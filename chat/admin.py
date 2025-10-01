from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Message, SEOSettings

# Временная переменная для отслеживания регистрации
_user_registered = False

class MessageInline(admin.TabularInline):
    model = Message
    fk_name = 'sender'
    extra = 0
    classes = ['collapse']

class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'date_joined', 'is_staff', 'is_active']
    list_editable = ['is_active']
    inlines = [MessageInline]

# Регистрируем модели только один раз
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, UserAdmin)

class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'content_short', 'message_type', 'timestamp', 'is_read']
    list_filter = ['message_type', 'timestamp', 'is_read']
    list_editable = ['is_read']
    search_fields = ['sender__username', 'receiver__username', 'content']
    readonly_fields = ['timestamp']

    def content_short(self, obj):
        return obj.content[:50] if obj.content else ''
    content_short.short_description = 'Сообщение'

admin.site.register(Message, MessageAdmin)

class SEOSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'site_description']
    
    def has_add_permission(self, request):
        # Разрешить создание только одной записи
        return not SEOSettings.objects.exists()

admin.site.register(SEOSettings, SEOSettingsAdmin)