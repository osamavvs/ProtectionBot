from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

router = Router()

# رقم الآيدي الخاص بك
ADMIN_ID = 8074717568

@router.message(Command("start"))
async def cmd_admin_start(message: Message):
    if message.from_user.id == ADMIN_ID:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="قفل المجموعة 🔒", callback_data="lock_group")],
            [InlineKeyboardButton(text="إحصائيات 📊", callback_data="stats")]
        ])
        await message.answer("🛠 **أهلاً بك يا أدمن، هذه لوحة التحكم:**", reply_markup=keyboard)
    else:
        await message.answer("أهلاً بك في بوت الحماية.")
