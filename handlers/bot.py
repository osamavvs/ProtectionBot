from pyrogram import Client
import os

# إعداد البوت
app = Client(
    "PyroHub",
    api_id=123456, # ضع الأرقام الخاصة بك
    api_hash="YOUR_HASH",
    bot_token="YOUR_TOKEN",
    plugins=dict(root="handlers") # هذا السطر هو سر سورس الموسوي (يقرأ كل الملفات تلقائياً)
)

print("البوت يعمل الآن بنظام الموسوي...")
app.run()
