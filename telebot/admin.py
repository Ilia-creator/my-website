from django.contrib import admin
from .models import TeleSettings, UserBotSettings

# Register your models here.
admin.site.register(TeleSettings)


@admin.register(UserBotSettings)
class UserBotSettingsAdmin(admin.ModelAdmin):
    readonly_fields = ('session_string',)
