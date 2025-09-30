from django.contrib.auth.models import User
from django.db import models

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'{self.sender} to {self.receiver}: {self.content[:20]}'

    @staticmethod
    def get_unread_count(user, sender):
        return Message.objects.filter(receiver=user, sender=sender, is_read=False).count()

# ПРОСТАЯ МОДЕЛЬ ДЛЯ SEO (без сложных полей)
class SEOSettings(models.Model):
    site_name = models.CharField('Название сайта', max_length=100, default='ElChat')
    site_description = models.TextField('Описание сайта', default='Бесплатный мессенджер для общения')

    def __str__(self):
        return "SEO Настройки"

    class Meta:
        verbose_name = 'SEO настройка'
        verbose_name_plural = 'SEO настройки'