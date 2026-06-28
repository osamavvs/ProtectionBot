from aiogram import Router, types, Bot
from config import ADMIN_ID
from db import get_users

router = Router()

bot_instance = None

def set_bot(bot: Bot):
    global bot_instance
    bot_instance = bot


@router.message(lambda m: m.text == "📢 إرسال رسالة")
async def ask_message(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer("✍️ اكتب الرسالة الآن وسيتم إرسالها للجميع")


@router.message()
async def broadcast(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    if message.text == "📢 إرسال رسالة":
        return

    users = get_users()

    sent = 0

    for user_id in users:
        try:
            await message.bot.send_message(user_id, message.text)
            sent += 1
        except:
            pass

    await message.answer(f"✅ تم الإرسال إلى {sent} مستخدم")
