from pyrogram import Client
import os

# إعداد البوت
app = Client(
    "PyroHub",
    api_id=123456, # ضع الأرقام الخاصة بك
    api_hash="5b8a468627791bdd36a8c361913b0b72",
    bot_token="8787399797:AAFFPGgLOqo7hY9hsfzya9XbTf79Ra0DsXU",
    plugins=dict(root="handlers") # هذا السطر هو سر سورس الموسوي (يقرأ كل الملفات تلقائياً)
)

print("البوت يعمل الآن بنظام الموسوي...")
app.run()
