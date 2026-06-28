import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

# استيراد الـ Routers من ملفات الـ handlers الخاصة بك
from handlers import commands, anti_spam, admin_panel

# تحميل المتغيرات السرية
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# إعداد نظام تسجيل الأخطاء (Logging)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def main():
    # التحقق من وجود التوكن
    if not TOKEN:
        logging.error("لم يتم العثور على BOT_TOKEN في ملف .env!")
        return

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # تسجيل جميع الراوترات (المدخلات)
    dp.include_router(commands.router)
    dp.include_router(anti_spam.router)
    dp.include_router(admin_panel.router)

    logging.info("البوت بدأ العمل بنجاح...")
    
    # تنظيف التحديثات القديمة قبل بدء البوت (لحماية البوت من الأخطاء عند التشغيل)
    await bot.delete_webhook(drop_pending_updates=True)
    
    # بدء تشغيل البوت
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("تم إيقاف البوت يدوياً.")
