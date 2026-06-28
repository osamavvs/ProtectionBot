import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from handlers import admin_panel, anti_spam

# ربط التوكن من إعدادات Railway (Variables)
TOKEN = os.getenv("TOKEN")

async def main():
    if not TOKEN:
        logging.error("خطأ: يرجى إضافة التوكن في إعدادات Variables في موقع Railway")
        return

    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    # ربط الراوترات التي تحتوي على الأوامر
    dp.include_router(admin_panel.router)
    dp.include_router(anti_spam.router)
    
    logging.info("البوت يعمل الآن بنجاح")
    
    # تنظيف التحديثات السابقة لبدء تشغيل نظيف
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("تم إيقاف البوت")
