import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# استدعاء ملفات الهاندلرز
from handlers import admin, start, callbacks

async def main():
    logging.basicConfig(level=logging.INFO)
    
    # السيرفر سيقرأ التوكن تلقائياً من متغيرات ريلواي باسم BOT_TOKEN
    # وإذا لم يجده سيستخدم التوكن الافتراضي المكتوب بالأسفل
    TOKEN = os.getenv("BOT_TOKEN", "8787399797:AAFFPGgLOqo7hY9hsfzya9XbTf79Ra0DsXU")

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    dp = Dispatcher()

    # ربط الملفات بالترتيب
    dp.include_router(start.router)      
    dp.include_router(admin.router)      
    dp.include_router(callbacks.router)  

    print("💎 سورس كرستال يعمل بنجاح وبدون أخطاء...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
