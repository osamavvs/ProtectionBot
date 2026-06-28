import asyncio
from aiogram import Bot, Dispatcher
from handlers import setup_routers # فقط استدعي هذه الدالة
from database import init_db

async def main():
    await init_db()
    bot = Bot(token="8787399797:AAFFPGgLOqo7hY9hsfzya9XbTf79Ra0DsXU")
    dp = Dispatcher()
    
    # ربط الراوترات باستخدام الدالة التي عرفناها في __init__.py
    setup_routers(dp)
    
    print("البوت يعمل الآن...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
