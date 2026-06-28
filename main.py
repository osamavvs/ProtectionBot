from pyrogram import Client, filters
from allGP import allGP # استدعاء الملف الذي وضعت فيه كودك
import redis

# إعدادات البوت
app = Client("my_bot", api_id=12345, api_hash="your_hash", bot_token="TOKEN")
r = redis.Redis(host='localhost', port=6379, db=0)

@app.on_message(filters.group)
async def handle_group(client, message):
    # تمرير الرسالة للكود الذي أرسلته لي
    allGP(client, message, r)

app.run()
