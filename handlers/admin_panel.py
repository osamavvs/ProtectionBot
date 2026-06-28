from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import os

router = Router()

# دالة لتجهيز لوحة الأدمن
def get_admin_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="قفل المجموعة 🔒", callback_data="lock_group")],
        [InlineKeyboardButton(text="إحصائيات 📊", callback_data="stats")]
    ])
    return keyboard

@router.message(Command("start"))
async def start_handler(message: Message):
    # الرقم الخاص بك الذي أرسلته
    ADMIN_ID = 8074717568
    
    # التحقق إذا كان المرسل هو أنت
    if message.from_user.id == ADMIN_ID:
        await message.answer(
            "🛠 **أهلاً بك يا مدير، هذه لوحة التحكم الخاصة بك:**", 
            reply_markup=get_admin_keyboard()
        )
    else:
        # رسالة ترحيب عادية للمستخدمين الآخرين
        await message.answer("أهلاً بك في بوت الحماية! نحن نعمل على تأمين المجموعة.")
