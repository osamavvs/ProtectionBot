import json
import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

router = Router()
ADMIN_ID = 8074717568
CONFIG_FILE = "settings.json"

# دالة لحفظ الحالة
def save_settings(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)

# دالة لقراءة الحالة
def load_settings():
    if not os.path.exists(CONFIG_FILE):
        return {"locked": False}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

@router.message(Command("start"), F.chat.type == "private")
async def start(message: Message):
    if message.from_user.id == ADMIN_ID:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="قفل المجموعة 🔒", callback_data="lock"), 
             InlineKeyboardButton(text="فتح المجموعة 🔓", callback_data="unlock")]
        ])
        await message.answer("🛠 **لوحة تحكم العمدة:**", reply_markup=kb)

@router.callback_query(F.data.in_(["lock", "unlock"]))
async def toggle_lock(call: CallbackQuery):
    settings = load_settings()
    if call.data == "lock":
        settings["locked"] = True
        await call.answer("تم قفل المجموعة 🔒")
    else:
        settings["locked"] = False
        await call.answer("تم فتح المجموعة 🔓")
    save_settings(settings)
