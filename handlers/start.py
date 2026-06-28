from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db import add_user
from config import ADMIN_ID

router = Router()

# 👑 لوحة الأدمن
admin_panel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📊 الإحصائيات", callback_data="stats")],
    [InlineKeyboardButton(text="📢 إرسال رسالة", callback_data="broadcast")],
    [InlineKeyboardButton(text="👥 المستخدمين", callback_data="users")]
])

# 👤 لوحة المستخدم
user_panel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="ℹ️ معلوماتي", callback_data="info")],
    [InlineKeyboardButton(text="🆘 مساعدة", callback_data="help")]
])


@router.message(CommandStart())
async def start(message: types.Message):

    # تسجيل المستخدم
    add_user(message.from_user.id)

    # 💎 ترحيب كرستال الكامل
    welcome_text = (
        "💎 أهلاً بك في Crystal Bot\n\n"
        "✨ نظام متكامل للإدارة والتحكم\n"
        "⚡ سرعة + حماية + أدوات قوية\n\n"
        "🔹 اختر من الأزرار بالأسفل"
    )

    if message.from_user.id == ADMIN_ID:
        await message.answer(
            "👑 أهلاً أدمن كرستال\n\n" + welcome_text,
            reply_markup=admin_panel
        )
    else:
        await message.answer(
            welcome_text,
            reply_markup=user_panel
        )
