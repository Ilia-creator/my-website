from .bot_api import get_manager_chat_id, send_message, edit_message_text, answer_callback_query
from .orders import order_text, order_keyboard, STATUS_LABELS

STATUS_ACTIONS = {
    'progress': STATUS_LABELS['progress'],
    'done': STATUS_LABELS['done'],
    'declined': STATUS_LABELS['declined'],
}


def is_authorized(chat_id):
    try:
        return str(chat_id) == get_manager_chat_id()
    except Exception:
        return False


def process_update(update):
    """Handle a single Telegram update dict, regardless of how it arrived
    (webhook POST body or getUpdates polling result)."""
    if 'callback_query' in update:
        _handle_callback(update['callback_query'])
    elif 'message' in update:
        _handle_message(update['message'])


def _handle_message(message):
    from crm.models import Order  # local import to avoid app-loading order issues

    chat_id = message.get('chat', {}).get('id')
    text = (message.get('text') or '').strip()

    if not is_authorized(chat_id):
        return

    if text == '/start':
        send_message(
            chat_id,
            "Бот заказов подключен ✅\n\n"
            "Команды:\n"
            "/orders — список новых заказов\n"
            "/order_<id> — карточка конкретного заказа, например /order_5"
        )
    elif text == '/orders':
        _send_orders_list(chat_id, Order)
    elif text.startswith('/order_'):
        order_id = text.replace('/order_', '').strip()
        _send_order_card(chat_id, order_id, Order)


def _send_orders_list(chat_id, Order, limit=10):
    closed_statuses = [STATUS_LABELS['done'], STATUS_LABELS['declined']]
    orders = (
        Order.objects.exclude(order_status__status_name__in=closed_statuses)
        .order_by('-order_dt')[:limit]
    )
    if not orders:
        send_message(chat_id, 'Новых заказов нет 🎉')
        return
    for order in orders:
        send_message(chat_id, order_text(order), reply_markup=order_keyboard(order))


def _send_order_card(chat_id, order_id, Order):
    order = Order.objects.filter(pk=order_id).first()
    if not order:
        send_message(chat_id, f'Заказ #{order_id} не найден')
        return
    send_message(chat_id, order_text(order), reply_markup=order_keyboard(order))


def _handle_callback(callback_query):
    from crm.models import Order, StatusCrm  # local import to avoid app-loading order issues

    chat_id = callback_query.get('message', {}).get('chat', {}).get('id')
    message_id = callback_query.get('message', {}).get('message_id')
    callback_id = callback_query.get('id')
    data = callback_query.get('data', '')

    if not is_authorized(chat_id):
        answer_callback_query(callback_id, 'Нет доступа')
        return

    try:
        _, order_id, action = data.split(':')
    except ValueError:
        answer_callback_query(callback_id)
        return

    order = Order.objects.filter(pk=order_id).first()
    if not order:
        answer_callback_query(callback_id, 'Заказ не найден')
        return

    status_name = STATUS_ACTIONS.get(action)
    if status_name:
        status, _created = StatusCrm.objects.get_or_create(status_name=status_name)
        order.order_status = status
        order.save()

    answer_callback_query(callback_id, f'Статус: {status_name}' if status_name else 'OK')

    if chat_id and message_id:
        edit_message_text(chat_id, message_id, order_text(order), reply_markup=order_keyboard(order))
