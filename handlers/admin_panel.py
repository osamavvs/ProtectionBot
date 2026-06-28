from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

router = Router()

# رقم الآيدي الخاص بك
ADMIN_ID = 8074717568

# الفلتر F.chat.type == "private" يضمن أن الأمر يعمل في الخاص فقط
@router.message(Command("start"), F.chat.type == "private")
async def cmd_admin_start(message: Message):
    if message.from_user.id == ADMIN_ID:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="قفل المجموعة 🔒", callback_data="lock_group")],
            [InlineKeyboardButton(text="إحصائيات 📊", callback_data="stats")]
        ])
        await message.answer("🛠 **أهلاً بك يا أدمن، هذه لوحة التحكم:**", reply_markup=keyboard)
    else:
        await message.answer("أهلاً بك في بوت الحماية. (هذا الأمر متاح للخاص فقط).")
