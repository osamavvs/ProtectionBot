import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from handlers.start import router as start_router
from handlers.protection import router as protection_router
from handlers.admin import router as admin_router

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

# 👇 ربط البوت مع الأدمن (مهم جداً)
set_bot(bot)

# تسجيل الراوترات
dp.include_router(start_router)
dp.include_router(protection_router)
dp.include_router(admin_router)

async def main():
    print("Bot is running 🚀")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
