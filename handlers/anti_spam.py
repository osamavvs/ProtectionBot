from aiogram import Router, F
from aiogram.types import Message
import json

router = Router()

def check_lock(key):
    try:
        with open("settings.json", "r") as f: return json.load(f).get(key, False)
    except: return False

@router.message(F.text.in_({"/mute", "/promote", "/ban"})) # مراقبة أوامر التيليجرام
async def watch_admins(message: Message):
    if message.from_user.id == 8074717568: return # استثناء المنشئ
    
    if check_lock("mute") and message.text == "/mute":
        await message.reply("ممنوع الكتم! المنشئ معطل هذه الصلاحية.")
        await message.delete()
    
    if check_lock("promote") and message.text == "/promote":
        await message.reply("ممنوع الرفع! المنشئ معطل هذه الصلاحية.")
        await message.delete()
