import json

from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .bot_api import get_token
from .handlers import process_update


@csrf_exempt
@require_POST
def telegram_webhook(request, token):
    # Only accept updates that include the bot's own token in the URL,
    # so random POSTs from the internet can't trigger anything.
    if token != get_token():
        return HttpResponseForbidden('invalid token')

    try:
        update = json.loads(request.body.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({'ok': False}, status=400)

    process_update(update)

    # Telegram just needs a 200 OK, content doesn't matter
    return JsonResponse({'ok': True})
