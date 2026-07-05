import json
import requests
from .models import TeleSettings


def _get_settings():
    return TeleSettings.objects.get(pk=1)


def get_token():
    return str(_get_settings().tg_token)


def get_manager_chat_id():
    return str(_get_settings().tg_chat)


def _api_url(method):
    return f'https://api.telegram.org/bot{get_token()}/{method}'


def send_message(chat_id, text, reply_markup=None):
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
    if reply_markup:
        payload['reply_markup'] = json.dumps(reply_markup)
    return requests.post(_api_url('sendMessage'), data=payload)


def edit_message_text(chat_id, message_id, text, reply_markup=None):
    payload = {'chat_id': chat_id, 'message_id': message_id, 'text': text, 'parse_mode': 'HTML'}
    if reply_markup:
        payload['reply_markup'] = json.dumps(reply_markup)
    return requests.post(_api_url('editMessageText'), data=payload)


def answer_callback_query(callback_query_id, text=None):
    payload = {'callback_query_id': callback_query_id}
    if text:
        payload['text'] = text
    return requests.post(_api_url('answerCallbackQuery'), data=payload)
