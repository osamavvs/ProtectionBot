import asyncio
from aiogram import Bot, Dispatcher
from handlers import admin, start, locks

async def main():
    bot = Bot(token="8787399797:AAFFPGgLOqo7hY9hsfzya9XbTf79Ra0DsXU")
    dp = Dispatcher()

    # تسجيل الراوترات (إضافة الأجزاء)
    dp.include_routers(start.router, admin.router, locks.router)

    print("البوت يعمل الآن يا أسامة...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
