from django.db import models

class UserBotSettings(models.Model):
    api_id = models.CharField(max_length=50, verbose_name='API ID')
    api_hash = models.CharField(max_length=100, verbose_name='API Hash')
    phone = models.CharField(max_length=30, verbose_name='Телефон')
    two_step_password = models.CharField(max_length=200, null=True, blank=True, verbose_name='Пароль 2FA')
    session_string = models.TextField(null=True, blank=True, verbose_name='Сессия (заполняется автоматически)')

    def __str__(self):
        return self.phone or f'UserBot #{self.pk}'

    class Meta:
        verbose_name = 'Настройку юзербота'
        verbose_name_plural = 'Настройки юзербота'


class TeleSettings(models.Model):
    tg_token = models.CharField(max_length=200, null=True, blank=True, verbose_name='Токен')
    tg_chat = models.CharField(max_length=200, null=True, blank=True, verbose_name='Чат айди')
    tg_message = models.TextField(null=True, blank=True, verbose_name='Текст сообщения')

    def __str__(self):
        return self.tg_chat or f'Settings #{self.pk}'

    class Meta:
        verbose_name = 'Настройку'
        verbose_name_plural = 'Настройки'
