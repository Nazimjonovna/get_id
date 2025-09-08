import json
import asyncio
from aiogram import types
from bot.bot_instance import bot, dp

async def handle(request):
    body = await request.body()
    update = types.Update.model_validate_json(body.decode("utf-8"))
    await dp.feed_update(bot, update)
    return {
        "statusCode": 200,
        "body": json.dumps({"ok": True})
    }

# For Vercel compatibility
def handler(request, context):
    return asyncio.run(handle(request))
