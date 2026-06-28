import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage  # <--- هذا السطر الناقص

from handlers import admin, start, callbacks, replies

async def main():
    logging.basicConfig(level=logging.INFO)
    
    TOKEN = os.getenv("BOT_TOKEN")

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    
    # تعريف الذاكرة المؤقتة وربطها بالـ Dispatcher
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # ربط الملفات
    dp.include_router(start.router)      
    dp.include_router(admin.router)      
    dp.include_router(replies.router)    
    dp.include_router(callbacks.router)  

    print("💎 سورس كرستال يعمل بنجاح وبأعلى استقرار...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
