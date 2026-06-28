import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import admin_panel, commands, anti_spam

# إعدادات البوت
TOKEN = "هنا_ضع_توكن_البوت_الخاص_بك"

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # تسجيل الراوترات (الترتيب: اللوحة أولاً)
    dp.include_router(admin_panel.router)
    dp.include_router(commands.router)
    dp.include_router(anti_spam.router)

    # تنظيف التحديثات القديمة وتشغيل البوت
    logging.info("البوت يعمل الآن بنجاح")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
