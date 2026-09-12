from django.core.management.base import BaseCommand, CommandError
from telethon import TelegramClient, events
from telethon.sessions import StringSession

from telebot.models import UserBotSettings


class Command(BaseCommand):
    help = (
        "Run the Telethon userbot (personal Telegram account autoresponder). "
        "Credentials and session are stored in the UserBotSettings row (pk=1), "
        "editable in Django admin. Stop with Ctrl+C."
    )

    def handle(self, *args, **options):
        try:
            settings_row = UserBotSettings.objects.get(pk=1)
        except UserBotSettings.DoesNotExist:
            raise CommandError(
                'UserBotSettings (pk=1) not found. Fill it in the admin first '
                '(api_id, api_hash, phone, two_step_password).'
            )

        app = TelegramClient(
            StringSession(settings_row.session_string or ''),
            settings_row.api_id,
            settings_row.api_hash,
        )

        @app.on(events.NewMessage())
        async def on_message(event: events.NewMessage.Event):
            print(event.chat_id, event.message.message)
            await event.message.reply('Hello from Telethon UserBot!')

        self.stdout.write(self.style.SUCCESS('App Started'))
        self.stdout.write(f'Phone: {settings_row.phone}')
        try:
            app.start(phone=settings_row.phone, password=settings_row.two_step_password)

            settings_row.session_string = app.session.save()
            settings_row.save(update_fields=['session_string'])

            app.run_until_disconnected()
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('App Finished'))
