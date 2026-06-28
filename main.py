import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# استدعاء جميع ملفات الهاندلرز الموزعة (بما فيها ملف الردود الجديد)
from handlers import admin, start, callbacks, replies

async def main():
    # إعدادات اللوج لمعرفة تفاصيل عمل السيرفر والأخطاء
    logging.basicConfig(level=logging.INFO)
    
    # قراءة التوكن من متغيرات بيئة ريلواي تلقائياً باسم BOT_TOKEN
    # وإذا لم يجده سيستخدم التوكن المكتوب كبديل للاختبار
    TOKEN = os.getenv("BOT_TOKEN", "هنا_تخلي_توكن_بوتك_الحقيقي")

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    dp = Dispatcher()

    # ربط الملفات بالترتيب الصحيح لمنع التضارب بين الفلاتر والردود
    dp.include_router(start.router)      # ملف الخاص والترحيب
    dp.include_router(admin.router)      # ملف أوامر الحماية والمنع للقروبات
    dp.include_router(replies.router)    # ملف نظام الردود التلقائية المنفصل (اضف رد / مسح رد)
    dp.include_router(callbacks.router)  # ملف الأزرار الشفافة وقوائم م1، م2 إلخ

    print("💎 سورس كرستال يعمل بنجاح وبأعلى استقرار...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
