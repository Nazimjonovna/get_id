import asyncio
from aiogram.client.default import DefaultBotProperties
import logging
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
# === CONFIGURATION ===
BOT_TOKEN = "7916797317:AAGr6pdkr17h0V59TVfD35b38JArK6VTzV0"
WEBHOOK_SECRET = "supersecret123"  # Change to a secret path
WEBHOOK_PATH = f"/webhook/{WEBHOOK_SECRET}"
WEBHOOK_URL = f"https://shakhlox.pythonanywhere.com{WEBHOOK_PATH}"
# === LOGGING ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# === BOT SETUP ===
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
# === HANDLERS ===
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_info = (
        f"👤 Sizning ma'lumotlaringiz:\n"
        f"🆔 ID: <code>{message.from_user.id}</code>\n"
        f"📛 Ism: {message.from_user.first_name}\n"
        f"👤 Familiya: {message.from_user.last_name or 'Yoʻq'}\n"
        f"🔗 Username: @{message.from_user.username or 'Yoʻq'}\n"
        f"💬 Chat ID: <code>{message.chat.id}</code>\n\n"
        f"📋 Ushbu ID ni .env faylida ADMIN_CHAT_ID ga qo'ying:\n"
        f"<code>ADMIN_CHAT_ID={message.from_user.id}</code>"
    )
    await message.answer(user_info)
@dp.message(Command("id"))
async def cmd_id(message: types.Message):
    chat_info = (
        f"💬 Chat turi: {message.chat.type}\n"
        f"🆔 Chat ID: <code>{message.chat.id}</code>\n"
        f"📛 Sarlavha: {message.chat.title or 'Shaxsiy chat'}\n"
        f"👤 Foydalanuvchi ID: <code>{message.from_user.id}</code>\n"
        f"📛 Foydalanuvchi ismi: {message.from_user.first_name}"
    )
    await message.answer(chat_info)
# === FLASK APP FOR WEBHOOK ===
app = Flask(__name__)

@app.route(WEBHOOK_PATH, methods=["POST"])
def handle_webhook():
    update = types.Update.model_validate_json(request.get_data().decode("utf-8"))
    asyncio.get_event_loop().create_task(dp.feed_update(bot, update))
    return "OK"
# === REQUIRED FOR WSGI ===
application = app
