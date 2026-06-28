import asyncio
from aiogram import Bot, Dispatcher
from handlers import admin, start, callbacks

# ضع التوكين الخاص بك هنا
API_TOKEN = '8787399797:AAFFPGgLOqo7hY9hsfzya9XbTf79Ra0DsXU'

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    # تسجيل الراوترات فقط (بدون الردود)
    dp.include_router(start.router)
    dp.include_router(admin.router)
    dp.include_router(callbacks.router)

    # بدء التشغيل
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
