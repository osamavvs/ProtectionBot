from aiogram import Router, F
from aiogram.types import Message
import json, os

router = Router()
ADMIN_ID = 8074717568
CONFIG_FILE = "settings.json"

def load():
    if not os.path.exists(CONFIG_FILE): return {"mute": False, "promote": False}
    with open(CONFIG_FILE, "r") as f: return json.load(f)

def save(data):
    with open(CONFIG_FILE, "w") as f: json.dump(data, f)

@router.message(F.text.in_({"تعطيل الكتم", "تفعيل الكتم", "تعطيل الرفع", "تفعيل الرفع"}))
async def control(message: Message):
    if message.from_user.id != ADMIN_ID: return
    data = load()
    if message.text == "تعطيل الكتم": data["mute"] = True
    elif message.text == "تفعيل الكتم": data["mute"] = False
    elif message.text == "تعطيل الرفع": data["promote"] = True
    elif message.text == "تفعيل الرفع": data["promote"] = False
    save(data)
    await message.reply(f"تم تنفيذ الأمر: {message.text}")
    await message.delete()
