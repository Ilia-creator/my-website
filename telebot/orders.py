from .bot_api import send_message, get_manager_chat_id

STATUS_LABELS = {
    'new': 'Новый',
    'progress': 'В работе',
    'done': 'Выполнен',
    'declined': 'Отклонён',
}


def order_text(order):
    package = order.order_package.pc_title if order.order_package else 'не указана'
    status = order.order_status.status_name if order.order_status else STATUS_LABELS['new']
    contact = order.get_order_contact_method_display() if order.order_contact_method else '—'
    return (
        f"<b>Заказ #{order.id}</b>\n"
        f"Имя: {order.order_name}\n"
        f"Телефон: {order.order_phone}\n"
        f"Связаться через: {contact}\n"
        f"Услуга: {package}\n"
        f"Статус: {status}"
    )


def order_keyboard(order):
    current = order.order_status.status_name if order.order_status else STATUS_LABELS['new']

    row1 = []
    if current != STATUS_LABELS['progress']:
        row1.append({'text': '▶️ В работу', 'callback_data': f'order:{order.id}:progress'})

    row2 = [
        {'text': '✅ Выполнен', 'callback_data': f'order:{order.id}:done'},
        {'text': '❌ Отклонить', 'callback_data': f'order:{order.id}:declined'},
    ]

    rows = []
    if row1:
        rows.append(row1)
    rows.append(row2)
    return {'inline_keyboard': rows}


def notify_new_order(order):
    """Send a new-order card with action buttons to the manager chat."""
    chat_id = get_manager_chat_id()
    return send_message(chat_id, order_text(order), reply_markup=order_keyboard(order))
