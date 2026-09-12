import os
import asyncio
from django.core.management.base import BaseCommand
from pyrogram import Client
from dotenv import load_workbook, load_dotenv  # Импортируем загрузчик

# Загружаем переменные из файла .env
load_dotenv()

API_ID = os.getenv("TELEGRAM_USERBOT_API_ID")
API_HASH = os.getenv("TELEGRAM_USERBOT_API_HASH")


class Command(BaseCommand):
    help = "Однократная авторизация юзербота прямо на сервере из .env"

    def handle(self, *args, **options):
        # Проверяем, что переменные загрузились
        if not API_ID or not API_HASH:
            self.stdout.write(
                self.style.ERROR("Ошибка: Ключи TELEGRAM_API_ID или TELEGRAM_API_HASH не найдены в .env!"))
            return

        self.stdout.write(self.style.SUCCESS("Запуск процесса авторизации..."))
        asyncio.run(self.run_auth())

    async def run_auth(self):
        # Преобразуем API_ID в int, так как из .env всё считывается как строка
        app = Client("user_shared_session", api_id=int(API_ID), api_hash=API_HASH)

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
