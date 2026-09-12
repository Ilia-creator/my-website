import asyncio
import logging
from django.core.management.base import BaseCommand
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from pyrogram import Client

# Настройка логирования в консоль сервера
logger = logging.getLogger(__name__)

# --- КОНФИГУРАЦИЯ ---
BOT_TOKEN = "ВАШ_ТОКЕН_ОФИЦИАЛЬНОГО_БОТА"
API_ID = 1234567
API_HASH = "ВАШ_API_HASH"

USER_CONFIG = {
    "targets": [],
    "message": "Привет! Это тестовая рассылка.",
    "interval": 5
}

MAILING_RUNNING = False


class MailingStates(StatesGroup):
    waiting_for_targets = State()
    waiting_for_message = State()
    waiting_for_interval = State()


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
user_client = Client("user_shared_session", api_id=API_ID, api_hash=API_HASH)


def get_main_menu():
    kb = [
        [KeyboardButton(text="🎯 Настроить получателей"), KeyboardButton(text="📝 Текст сообщения")],
        [KeyboardButton(text="⏱ Интервал"), KeyboardButton(text="📊 Показать настройки")],
        [KeyboardButton(text="🚀 ЗАПУСТИТЬ"), KeyboardButton(text="🛑 ОСТАНОВИТЬ")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


# --- ОБРАБОТЧИКИ AIOGRAM ---

@dp.message(F.text == "/start")
@dp.message(F.text == "Главное меню")
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Бот запущен на Django-сервере и готов к работе.", reply_markup=get_main_menu())


@dp.message(F.text == "📊 Показать настройки")
async def show_settings(message: Message):
    targets_str = ", ".join(USER_CONFIG["targets"]) if USER_CONFIG["targets"] else "Не настроены"
    status = "✅ Активен" if user_client and user_client.is_connected else "❌ Не подключен"
    running_status = "🏃 Работает" if MAILING_RUNNING else "⏸ Стоит"

    text = (
        f"⚙️ **Текущие настройки:**\n\n"
        f"Статус аккаунта: {status}\n"
        f"Статус рассылки: {running_status}\n"
        f"Интервал: {USER_CONFIG['interval']} сек.\n"
        f"Получатели: {targets_str}\n"
        f"Текст: {USER_CONFIG['message']}"
    )
    await message.answer(text, parse_mode="Markdown")


@dp.message(F.text == "🎯 Настроить получателей")
async def set_targets(message: Message, state: FSMContext):
    await message.answer("Введите список @username через запятую:")
    await state.set_state(MailingStates.waiting_for_targets)


@dp.message(MailingStates.waiting_for_targets)
async def process_targets(message: Message, state: FSMContext):
    raw_targets = message.text.split(",")
    USER_CONFIG["targets"] = [t.strip() for t in raw_targets if t.strip()]
    await message.answer(f"✅ Сохранено получателей: {len(USER_CONFIG['targets'])}", reply_markup=get_main_menu())
    await state.clear()


@dp.message(F.text == "📝 Текст сообщения")
async def set_message(message: Message, state: FSMContext):
    await message.answer("Введите текст рассылки:")
    await state.set_state(MailingStates.waiting_for_message)


@dp.message(MailingStates.waiting_for_message)
async def process_message(message: Message, state: FSMContext):
    USER_CONFIG["message"] = message.text
    await message.answer("✅ Текст изменен.", reply_markup=get_main_menu())
    await state.clear()


@dp.message(F.text == "⏱ Интервал")
async def set_interval(message: Message, state: FSMContext):
    await message.answer("Введите интервал в секундах:")
    await state.set_state(MailingStates.waiting_for_interval)


@dp.message(MailingStates.waiting_for_interval)
async def process_interval(message: Message, state: FSMContext):
    try:
        USER_CONFIG["interval"] = int(message.text.strip())
        await message.answer(f"✅ Интервал: {USER_CONFIG['interval']} сек.", reply_markup=get_main_menu())
    except ValueError:
        await message.answer("Введите целое число.")
    await state.clear()


@dp.message(F.text == "🛑 ОСТАНОВИТЬ")
async def stop_mailing(message: Message):
    global MAILING_RUNNING
    if not MAILING_RUNNING:
        await message.answer("Рассылка и так не работает.")
        return
    MAILING_RUNNING = False
    await message.answer("🛑 Сигнал на остановку отправлен. Текущий круг завершится или прервется.")


@dp.message(F.text == "🚀 ЗАПУСТИТЬ")
async def start_mailing(message: Message):
    global user_client, MAILING_RUNNING

    if not user_client or not user_client.is_connected:
        await message.answer(
            "❌ Юзербот не активен. Убедитесь, что сессия user_shared_session.session лежит в корне проекта.")
        return
    if not USER_CONFIG["targets"]:
        await message.answer("❌ Список получателей пуст.")
        return
    if MAILING_RUNNING:
        await message.answer("⚠️ Рассылка уже запущена!")
        return

    MAILING_RUNNING = True
    await message.answer("🚀 Бесконечная рассылка запущена!")

    loop_count = 1
    while MAILING_RUNNING:
        await message.answer(f"📦 Начался круг рассылки №{loop_count}")

        for target in USER_CONFIG["targets"]:
            if not MAILING_RUNNING:
                break

            try:
                await user_client.send_message(target, USER_CONFIG["message"])
                await message.answer(f"🔹 Отправлено на {target}")
            except Exception as e:
                await message.answer(f"⚠️ Ошибка на {target}: {e}")

            await asyncio.sleep(USER_CONFIG["interval"])

        loop_count += 1
        await asyncio.sleep(10)


# --- ГЛАВНЫЙ КЛАСС КОМАНДЫ DJANGO ---
class Command(BaseCommand):
    help = "Запуск Telegram бота рассылки внутри Django"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Инициализация асинхронного запуска..."))
        try:
            asyncio.run(self.run_bot())
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("Бот остановлен пользователем."))

    async def run_bot(self):
        # Запускаем Pyrogram юзербота
        await user_client.start()
        # Запускаем Aiogram панель управления
        await dp.start_polling(bot)
