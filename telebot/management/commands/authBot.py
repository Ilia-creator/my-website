import asyncio
from django.core.management.base import BaseCommand
from pyrogram import Client

# Вставьте ваши данные с my.telegram.org
API_ID = 1234567  # Ваше число api_id
API_HASH = "ВАШ_ХЭШ"  # Ваш api_hash


class Command(BaseCommand):
    help = "Однократная авторизация юзербота прямо на сервере"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Запуск процесса авторизации..."))
        asyncio.run(self.run_auth())

    async def run_auth(self):
        # Создает сессию ровно с тем же именем, что использует основной бот
        app = Client("user_shared_session", api_id=API_ID, api_hash=API_HASH)

        self.stdout.write(self.style.WARNING(
            "\nСейчас Telegram запросит ваш номер телефона и код подтверждения.\n"
            "Если код содержит буквы, вводите их с учетом регистра.\n"
        ))

        async with app:
            me = await app.get_me()
            self.stdout.write(self.style.SUCCESS(
                f"\n🎉 УСПЕХ! Вы авторизовались как: {me.first_name} (@{me.username or 'нет юзернейма'})\n"
                f"Файл сессии успешно создан в корне проекта на сервере."
            ))
