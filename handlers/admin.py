from aiogram import Router, types
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from db import get_users
from config import ADMIN_ID

router = Router()

# 🔙 زر رجوع
def main_panel():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 الإحصائيات", callback_data="stats")],
        [InlineKeyboardButton(text="📢 إرسال رسالة", callback_data="broadcast")],
        [InlineKeyboardButton(text="👥 المستخدمين", callback_data="users")]
    ])


# 📊 الإحصائيات
@router.callback_query(lambda c: c.data == "stats")
async def stats(call: CallbackQuery):

    if call.from_user.id != ADMIN_ID:
        return

    users = len(get_users())

    await call.message.edit_text(
        f"💎 Crystal Stats\n\n👥 عدد المستخدمين: {users}",
        reply_markup=main_panel()
    )


# 👥 المستخدمين
@router.callback_query(lambda c: c.data == "users")
async def users(call: CallbackQuery):

    if call.from_user.id != ADMIN_ID:
        return

    await call.message.edit_text(
        f"👥 Crystal Users\n\nعدد المستخدمين: {len(get_users())}",
        reply_markup=main_panel()
    )


# 📢 إرسال رسالة
@router.callback_query(lambda c: c.data == "broadcast")
async def broadcast(call: CallbackQuery):

    if call.from_user.id != ADMIN_ID:
        return

    await call.message.answer("✍️ اكتب الرسالة الآن لإرسالها لجميع المستخدمين")

    @router.message()
    async def send_all(message: types.Message):

        if message.from_user.id != ADMIN_ID:
            return

        users = get_users()
        sent = 0

        for
