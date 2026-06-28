from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
import json, os

router = Router()
ADMIN_ID = 8074717568
CONFIG_FILE = "settings.json"

# دالة لتحميل الإعدادات
def load():
    if not os.path.exists(CONFIG_FILE): return {"mute": False, "promote": False, "locked": False}
    with open(CONFIG_FILE, "r") as f: return json.load(f)

# دالة لحفظ الإعدادات
def save(data):
    with open(CONFIG_FILE, "w") as f: json.dump(data, f)

# إظهار الأوامر عند كتابة "الاوامر"
@router.message(F.text == "الاوامر")
async def show_commands(message: Message):
    if message.from_user.id != ADMIN_ID: return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="تعطيل الكتم", callback_data="mute_off"), 
         InlineKeyboardButton(text="تفعيل الكتم", callback_data="mute_on")],
        [InlineKeyboardButton(text="تعطيل الرفع", callback_data="promote_off"), 
         InlineKeyboardButton(text="تفعيل الرفع", callback_data="promote_on")],
        [InlineKeyboardButton(text="قفل المجموعة", callback_data="lock"), 
         InlineKeyboardButton(text="فتح المجموعة", callback_data="unlock")]
    ])
    
    await message.reply("📋 **أوامر المجموعة:**\n\nاختر الأمر الذي تريد تنفيذه:", reply_markup=keyboard)
    await message.delete()

# معالجة الأزرار
@router.callback_query(F.data.in_(["mute_off", "mute_on", "promote_off", "promote_on", "lock", "unlock"]))
async def handle_buttons(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("هذا الأمر للمنشئ فقط 🚫", show_alert=True)
        return
    
    data = load()
    action = callback.data
    
    if action == "mute_off": data["mute"] = True
    elif action == "mute_on": data["mute"] = False
    elif action == "promote_off": data["promote"] = True
    elif action == "promote_on": data["promote"] = False
    elif action == "lock": data["locked"] = True
    elif action == "unlock": data["locked"] = False
    
    save(data)
    await callback.answer(f"تم تنفيذ: {action}")
