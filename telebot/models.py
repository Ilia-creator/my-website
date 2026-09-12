from django.db import models

class TeleSettings(models.Model):
    tg_token = models.CharField(max_length=200, null=True, blank=True, verbose_name='Токен')
    tg_chat = models.CharField(max_length=200, null=True, blank=True, verbose_name='Чат айди')
    tg_message = models.TextField(null=True, blank=True, verbose_name='Текст сообщения')

    def __str__(self):
        return self.tg_chat or f'Settings #{self.pk}'

    class Meta:
        verbose_name = 'Настройку'
        verbose_name_plural = 'Настройки'
