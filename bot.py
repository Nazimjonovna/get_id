import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiohttp import web

# === CONFIGURATION ===
BOT_TOKEN = "7916797317:AAGr6pdkr17h0V59TVfD35b38JArK6VTzV0"
WEBHOOK_SECRET = "supersecret123"
WEBHOOK_PATH = f"/webhook/{WEBHOOK_SECRET}"
WEBHOOK_URL = f"https://get-id-production.up.railway.app/webhook/supersecret123"

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

# === AIOHTTP WEBHOOK SERVER ===
async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL)
    logger.info(f"Webhook set to: {WEBHOOK_URL}")


async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
    logger.info("Webhook deleted")


async def webhook_handler(request: web.Request):
    body = await request.read()
    update = types.Update.model_validate_json(body.decode('utf-8'))
    await dp.feed_update(bot, update)
    return web.Response(text="OK")


def create_app():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, webhook_handler)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), port=8000)
