import os
import asyncio
from django.core.management.base import BaseCommand
from pyrogram import Client

# Берем переменные НАПРЯМУЮ из системы (Portainer передает их именно сюда)
API_ID = os.getenv("TELEGRAM_USERBOT_API_ID")
API_HASH = os.getenv("TELEGRAM_USERBOT_API_HASH")


class Command(BaseCommand):
    help = "Однократная авторизация юзербота прямо на сервере"

    def handle(self, *args, **options):
        # Проверяем, передались ли переменные из Portainer
        if not API_ID or not API_HASH:
            self.stdout.write(self.style.ERROR(
                "❌ Ошибка: Переменные TELEGRAM_USERBOT_API_ID или TELEGRAM_USERBOT_API_HASH не найдены!\n"
                "Убедитесь, что вы добавили их в настройках контейнера в Portainer (раздел Environment variables) и перезапустили контейнер."
            ))
            return

        self.stdout.write(self.style.SUCCESS("Запуск процесса авторизации..."))
        asyncio.run(self.run_auth())

    async def run_auth(self):
        # Преобразуем API_ID в int
        app = Client("user_shared_session", api_id=int(API_ID), api_hash=API_HASH)

        self.stdout.write(self.style.WARNING(
            "\nСейчас Telegram запросит ваш номер телефона и код подтверждения.\n"
            "Вводите данные прямо сюда в консоль Portainer.\n"
        ))

        async with app:
            me = await app.get_me()
            self.stdout.write(self.style.SUCCESS(
                f"\n🎉 УСПЕХ! Вы авторизовались как: {me.first_name} (@{me.username or 'нет юзернейма'})\n"
                f"Файл сессии успешно создан в контейнере."
            ))
