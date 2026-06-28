from aiogram import Router, F
from aiogram.types import Message
import json
import os

router = Router()

def is_locked():
    if not os.path.exists("settings.json"): return False
    with open("settings.json", "r") as f:
        return json.load(f).get("locked", False)

@router.message(F.chat.type.in_({"group", "supergroup"}))
async def group_handler(message: Message):
    # استثناء الأدمن من القفل
    if message.from_user.id == 8074717568:
        return
        
    if is_locked():
        try:
            await message.delete()
        except:
            pass
