from pyrogram import Client
import os

# تشغيل البوت مع ربط المجلد (handlers)
app = Client(
    "ProtectionBot",
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH"),
    bot_token=os.environ.get("BOT_TOKEN"),
    plugins=dict(root="handlers") 
)

if __name__ == "__main__":
    print("ProtectionBot is starting...")
    app.run()
