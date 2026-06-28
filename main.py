from pyrogram import Client

app = Client(
    "ProtectionBot",
    api_id=24752047,             # ضع رقمك الحقيقي هنا
    api_hash="5b8a468627791bdd36a8c361913b0b72",   # ضع الـ Hash الحقيقي هنا
    bot_token="8787399797:AAFFPGgLOqo7hY9hsfzya9XbTf79Ra0DsXU", # ضع التوكن الحقيقي هنا
    plugins=dict(root="handlers")
)

app.run()
