import time

import requests
from django.core.management.base import BaseCommand

from telebot.models import TeleSettings
from telebot.handlers import process_update


class Command(BaseCommand):
    help = (
        "Run the Telegram bot in polling mode for local development. "
        "No public HTTPS / ngrok needed — works fine on plain localhost. "
        "Stop with Ctrl+C. Don't run this together with the webhook in production "
        "at the same time (Telegram only delivers updates one way at once)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--timeout', type=int, default=30,
            help='Long-polling timeout in seconds passed to getUpdates (default: 30)',
        )

    def handle(self, *args, **options):
        try:
            ts = TeleSettings.objects.get(pk=1)
        except TeleSettings.DoesNotExist:
            self.stderr.write(self.style.ERROR(
                'TeleSettings (pk=1) not found. Fill it in the admin first (token, chat id, message template).'
            ))
            return

        token = str(ts.tg_token)
        timeout = options['timeout']
        api_url = f'https://api.telegram.org/bot{token}/getUpdates'

        # Make sure no webhook is set, otherwise Telegram refuses to deliver
        # updates via getUpdates at the same time.
        requests.post(f'https://api.telegram.org/bot{token}/deleteWebhook')

        self.stdout.write(self.style.SUCCESS(
            'Polling started. Write /start to the bot in your manager chat. Press Ctrl+C to stop.'
        ))

        offset = None
        while True:
            try:
                params = {'timeout': timeout}
                if offset is not None:
                    params['offset'] = offset

                resp = requests.get(api_url, params=params, timeout=timeout + 10)
                data = resp.json()

                if not data.get('ok'):
                    self.stderr.write(self.style.ERROR(f'Telegram API error: {data}'))
                    time.sleep(3)
                    continue

                for update in data.get('result', []):
                    offset = update['update_id'] + 1
                    try:
                        process_update(update)
                    except Exception as e:
                        self.stderr.write(self.style.ERROR(f'Error handling update: {e}'))

            except KeyboardInterrupt:
                self.stdout.write(self.style.WARNING('\nPolling stopped.'))
                break
            except requests.RequestException as e:
                self.stderr.write(self.style.ERROR(f'Network error: {e}, retrying in 3s'))
                time.sleep(3)
