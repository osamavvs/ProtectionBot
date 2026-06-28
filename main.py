import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# استدعاء ملفات الهاندلرز (الأوامر والـ Callbacks)
from handlers import admin, start, callbacks

# توكن البوت الخاص بك (تأكد من وضعه في إعدادات Railway أو استبداله هنا)
TOKEN = "YOUR_BOT_TOKEN_HERE"

async def main():
    # إعدادات اللوج لمعرفة الأخطاء إن وجدت
    logging.basicConfig(level=logging.INFO)
    
    # تشغيل البوت مع دعم صيغة الماركداون والـ HTML تلقائياً
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    dp = Dispatcher()

    # ربط الملفات بالترتيب الصحيح لضمان عمل الفلاتر بدون تضارب
    dp.include_router(start.router)      # ملف الخاص بالمطور
    dp.include_router(admin.router)      # ملف أوامر المجموعات
    dp.include_router(callbacks.router)  # ملف أزرار التحكم الشفافة { 1 } والرجوع

    # بدء تشغيل البوت واستقبال الرسائل
    print("💎 سورس كرستال يعمل بنجاح وبدون أخطاء...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
