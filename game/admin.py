from django.contrib import admin
from .models import PlayerProgress

@admin.register(PlayerProgress)
class PlayerProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'money', 'money_per_click', 'autoclicker_level', 'last_save')
    list_filter = ('autoclicker_level',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('last_save',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('user',)
        }),
        ('Статистика игрока', {
            'fields': ('money', 'money_per_click', 'autoclicker_level')
        }),
        ('Служебное', {
            'fields': ('last_save',),
        }),
    )
