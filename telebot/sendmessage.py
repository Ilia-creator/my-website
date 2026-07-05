import requests
from .models import TeleSettings


def sendTelegram(tg_name, tg_phone, tg_package=None):
    """
    Send an order notification to Telegram.
    The message template (TeleSettings.tg_message) can use named placeholders:
        {name}, {phone}, {package}
    Older templates that only use {} for name/phone are also supported for
    backwards compatibility.
    """
    settings = TeleSettings.objects.get(pk=1)
    token = str(settings.tg_token)
    chat_id = str(settings.tg_chat)
    template = str(settings.tg_message)
    package_text = tg_package if tg_package else 'не указана'

    api = 'https://api.telegram.org/bot'
    method = api + token + '/sendMessage'

    if '{name}' in template or '{phone}' in template or '{package}' in template:
        # New-style template with named placeholders
        text_slice = template.format(name=tg_name, phone=tg_phone, package=package_text)
    else:
        # Legacy template using two positional {} placeholders (name, phone)
        a = template.find('{')
        b = template.find('}')
        c = template.rfind('{')
        d = template.rfind('}')

        part_1 = template[0:a]
        part_2 = template[b + 1:c]
        part_3 = template[d:-1]

        text_slice = part_1 + tg_name + part_2 + tg_phone + part_3
        text_slice += f"\nУслуга: {package_text}"

    requests.post(method, data={
        'chat_id': chat_id,
        'text': text_slice,
    })
