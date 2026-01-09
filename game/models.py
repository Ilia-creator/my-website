from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class PlayerProgress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    money = models.IntegerField(default=0)
    money_per_click = models.IntegerField(default=1)
    autoclicker_level = models.IntegerField(default=0)
    last_save = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user.username} — ${self.money:,.0f}"

    class Meta:
        verbose_name = "Прогресс игрока"
        verbose_name_plural = "Прогресс игроков"
