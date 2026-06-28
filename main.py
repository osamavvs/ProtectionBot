import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

# استيراد الـ Routers
from handlers import commands, anti_spam, admin_panel

# تحميل المتغيرات: إذا وجد ملف .env يحمله، إذا لم يجده يعتمد على متغيرات النظام (Railway)
if os.path.exists(".env"):
    load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# إعداد نظام تسجيل الأخطاء
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def main():
    # التحقق من وجود التوكن
    if not TOKEN:
        logging.error("خطأ: لم يتم العثور على BOT_TOKEN في المتغيرات!")
        return

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # تسجيل جميع الراوترات
    dp.include_router(commands.router)
    dp.include_router(anti_spam.router)
    dp.include_router(admin_panel.router)

    logging.info("البوت يعمل الآن بنجاح...")
    
    # تنظيف التحديثات القديمة
    await bot.delete_webhook(drop_pending_updates=True)
    
    # بدء تشغيل البوت
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("تم إيقاف البوت يدوياً.")
