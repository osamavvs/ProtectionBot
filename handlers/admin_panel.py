from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(Command("start"))
async def admin_start(message: Message):
    # السورس غالباً يستخدم معرف ثابت للأدمن
    ADMIN_ID = 8074717568
    
    if message.from_user.id == ADMIN_ID:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="قفل المجموعة 🔒", callback_data="lock")],
            [InlineKeyboardButton(text="التحكم ⚙️", callback_data="settings")]
        ])
        await message.answer("أهلاً بك يا أدمن في لوحة التحكم:", reply_markup=keyboard)
    else:
        await message.answer("أهلاً بك في البوت.")
