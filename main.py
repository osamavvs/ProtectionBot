import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from handlers import admin_panel, anti_spam, extras, id_card # تأكد من إضافة id_card

TOKEN = os.getenv("TOKEN")

async def main():
    if not TOKEN:
        logging.error("يرجى إضافة التوكن في Variables في Railway")
        return
    
    bot = Bot(token=TOKEN)
    dp = Dispatcher() # التعريف هنا مهم جداً
    
    # الآن يمكننا استخدام dp لإضافة الروابط
    dp.include_router(admin_panel.router)
    dp.include_router(anti_spam.router)
    dp.include_router(extras.router)
    dp.include_router(id_card.router) 
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
