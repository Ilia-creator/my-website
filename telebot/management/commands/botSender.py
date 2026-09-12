import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from dotenv import load_dotenv
from telethon import TelegramClient, events

SESSION_PATH = os.path.join(settings.BASE_DIR, 'telebot', 'Telethon_UserBot')
ENV_PATH = os.path.join(settings.BASE_DIR, 'telebot', '.env.userbot')


class Command(BaseCommand):
    help = (
        "Run the Telethon userbot (personal Telegram account autoresponder). "
        "Credentials come from TELEGRAM_USERBOT_API_ID / TELEGRAM_USERBOT_API_HASH / "
        "TELEGRAM_USERBOT_PHONE / TELEGRAM_USERBOT_2FA_PASSWORD in telebot/.env.userbot "
        "(local only, never committed — see .gitignore). Stop with Ctrl+C."
    )

    def handle(self, *args, **options):
        load_dotenv(ENV_PATH)

        api_id = os.getenv('TELEGRAM_USERBOT_API_ID')
        api_hash = os.getenv('TELEGRAM_USERBOT_API_HASH')
        phone = os.getenv('TELEGRAM_USERBOT_PHONE')
        password = os.getenv('TELEGRAM_USERBOT_2FA_PASSWORD')

        if not api_id or not api_hash or not phone:
            raise CommandError(
                'TELEGRAM_USERBOT_API_ID / TELEGRAM_USERBOT_API_HASH / TELEGRAM_USERBOT_PHONE '
                'must be set in telebot/.env.userbot'
            )

        app = TelegramClient(SESSION_PATH, api_id, api_hash)

        @app.on(events.NewMessage())
        async def on_message(event: events.NewMessage.Event):
            print(event.chat_id, event.message.message)
            await event.message.reply('Hello from Telethon UserBot!')

        self.stdout.write(self.style.SUCCESS('App Started'))
        try:
            app.start(phone=phone, password=password)
            app.run_until_disconnected()
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('App Finished'))
