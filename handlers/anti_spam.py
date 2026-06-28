from aiogram import Router, F
from aiogram.types import Message
import json

router = Router()

@router.message(F.text.in_({"/mute", "/promote"}))
async def check_commands(message: Message):
    if message.from_user.id == 8074717568: return
    with open("settings.json", "r") as f: data = json.load(f)
    if (data.get("mute") and message.text == "/mute") or (data.get("promote") and message.text == "/promote"):
        await message.reply("هذه الصلاحية معطلة من قبل المنشئ!")
        await message.delete()
