import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

# استدعاء ملفات الـ Handlers
from handlers import replies, admin, start, callbacks

async def main():
    logging.basicConfig(level=logging.INFO)
    
    TOKEN = os.getenv("BOT_TOKEN")

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # الترتيب مهم جداً:
    # نضع replies أولاً لكي يفحص الردود قبل أن تتدخل الحماية (admin)
    dp.include_router(replies.router)    
    dp.include_router(admin.router)      
    dp.include_router(start.router)      
    dp.include_router(callbacks.router)  

    print("💎 سورس كرستال يعمل بنجاح...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
