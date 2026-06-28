from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

router = Router()
ADMIN_ID = 8074717568

@router.message(F.text == "الاوامر")
async def show_commands(message: Message):
    # ترتيب الأزرار لتبدو احترافية
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

# معالجة ضغط الأزرار
@router.callback_query(F.data.in_(["mute_off", "mute_on", "promote_off", "promote_on", "lock", "unlock"]))
async def handle_buttons(callback: callback_query):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("هذا الأمر للمنشئ فقط 🚫", show_alert=True)
        return
    
    # هنا يتم تنفيذ الوظيفة بناءً على الزر
    action = callback.data
    await callback.answer(f"تم تنفيذ: {action}")
