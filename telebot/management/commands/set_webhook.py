import requests
from django.core.management.base import BaseCommand
from telebot.models import TeleSettings


class Command(BaseCommand):
    help = (
        "Register the Telegram bot webhook so updates from Telegram are sent to this site. "
        "Usage: python manage.py set_webhook https://your-domain.com"
    )

    def add_arguments(self, parser):
        parser.add_argument('base_url', type=str, help='Public site URL, e.g. https://shubnikov.me')

    def handle(self, *args, **options):
        base_url = options['base_url'].rstrip('/')

        try:
            ts = TeleSettings.objects.get(pk=1)
        except TeleSettings.DoesNotExist:
            self.stderr.write(self.style.ERROR(
                'TeleSettings (pk=1) not found. Fill it in the admin first (token, chat id, message template).'
            ))
            return

        token = str(ts.tg_token)
        webhook_url = f'{base_url}/telebot/webhook/{token}/'

        resp = requests.post(
            f'https://api.telegram.org/bot{token}/setWebhook',
            data={'url': webhook_url},
        )

        self.stdout.write(f'Webhook URL: {webhook_url}')
        self.stdout.write(resp.text)

        if resp.ok and resp.json().get('ok'):
            self.stdout.write(self.style.SUCCESS('Webhook registered successfully.'))
        else:
            self.stderr.write(self.style.ERROR('Failed to register webhook, see response above.'))
