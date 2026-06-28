from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db import add_user
from config import ADMIN_ID

router = Router()

# 👑 لوحة العمدة
admin_panel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📊 الإحصائيات", callback_data="stats")],
    [InlineKeyboardButton(text="📢 إرسال رسالة", callback_data="broadcast")],
    [InlineKeyboardButton(text="👥 المستخدمين", callback_data="users")],
    [InlineKeyboardButton(text="⚙️ إعدادات", callback_data="settings")]
])

# 👤 المستخدم
user_panel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="ℹ️ معلوماتي", callback_data="info")]
])

@router.message()
async def start(message: types.Message):

    if message.text == "/start":

        add_user(message.from_user.id)

        if message.from_user.id == ADMIN_ID:
            await message.answer("👑 لوحة العمدة:", reply_markup=admin_panel)
        else:
            await message.answer("👋 أهلاً بيك", reply_markup=user_panel)
