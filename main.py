import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import admin_panel, anti_spam

async def main():
    bot = Bot(token="ضع_التوكن_هنا") # ضع التوكن هنا
    dp = Dispatcher()
    dp.include_router(admin_panel.router)
    dp.include_router(anti_spam.router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
