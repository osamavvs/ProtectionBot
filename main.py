import asyncio
from aiogram import Bot, Dispatcher
from handlers import admin, start, locks
from database import init_db # استيراد دالة الإنشاء

async def main():
    await init_db() # تشغيل قاعدة البيانات عند بدء البوت
    bot = Bot(token="8787399797:AAFFPGgLOqo7hY9hsfzya9XbTf79Ra0DsXU")
    dp = Dispatcher()

    dp.include_routers(start.router, admin.router, locks.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
