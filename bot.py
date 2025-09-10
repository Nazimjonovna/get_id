import os
import logging
import asyncio

from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

# === CONFIG ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "supersecret123")
BASE_WEBHOOK_URL = os.getenv("WEBHOOK_BASE", "https://get-id-production.up.railway.app")
WEBHOOK_PATH = f"/webhook/{WEBHOOK_SECRET}"
WEBHOOK_URL = f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}"
PORT = int(os.getenv("PORT", 8000))  # Railway gives you this

# === LOGGING ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === BOT SETUP ===
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# === HANDLERS ===
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        f"👤 Sizning ma'lumotlaringiz:\n"
        f"🆔 ID: <code>{message.from_user.id}</code>\n"
        f"📛 Ism: {message.from_user.first_name}\n"
        f"👤 Familiya: {message.from_user.last_name or 'Yoʻq'}\n"
        f"🔗 Username: @{message.from_user.username or 'Yoʻq'}\n"
        f"💬 Chat ID: <code>{message.chat.id}</code>\n\n"
        f"📋 Ushbu ID ni .env faylida ADMIN_CHAT_ID ga qo'ying:\n"
        f"<code>ADMIN_CHAT_ID={message.from_user.id}</code>"
    )

@dp.message(Command("id"))
async def id_handler(message: types.Message):
    await message.answer(
        f"💬 Chat turi: {message.chat.type}\n"
        f"🆔 Chat ID: <code>{message.chat.id}</code>\n"
        f"📛 Sarlavha: {message.chat.title or 'Shaxsiy chat'}\n"
        f"👤 Foydalanuvchi ID: <code>{message.from_user.id}</code>\n"
        f"📛 Foydalanuvchi ismi: {message.from_user.first_name}"
    )

# === WEBHOOK HANDLER ===
async def handle_webhook(request: web.Request):
    body = await request.read()
    update = types.Update.model_validate_json(body.decode("utf-8"))
    await dp.feed_update(bot, update)
    return web.Response(text="OK")

# === STARTUP & SHUTDOWN ===
async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL)
    logger.info(f"Webhook set: {WEBHOOK_URL}")

async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
    logger.info("Webhook deleted")

# === APP CREATION ===
def create_app():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_webhook)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app

# === MAIN ENTRY ===
if __name__ == "__main__":
    web.run_app(create_app(), port=PORT)
