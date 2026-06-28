from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db import add_user
from config import ADMIN_ID

router = Router()

# لوحة الأدمن (أزرار داخل الرسالة)
admin_panel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📢 إرسال رسالة", callback_data="send")],
    [InlineKeyboardButton(text="👥 عدد المستخدمين", callback_data="users")],
    [InlineKeyboardButton(text="🚫 حظر مستخدم", callback_data="ban")]
])

@router.message(CommandStart())
async def start(message: types.Message):

    add_user(message.from_user.id)

    if message.from_user.id == ADMIN_ID:
        await message.answer("👑 لوحة الأدمن:", reply_markup=admin_panel)
    else:
        await message.answer("👋 أهلاً بيك\nالبوت شغال 🔥")
