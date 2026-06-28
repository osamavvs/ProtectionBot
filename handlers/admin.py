from aiogram import Router, types
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from db import get_users
from config import ADMIN_ID

router = Router()

# 🔙 زر رجوع
back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔙 رجوع", callback_data="back")]
])

# 📊 الإحصائيات
@router.callback_query(lambda c: c.data == "stats")
async def stats(call: CallbackQuery):

    if call.from_user.id != ADMIN_ID:
        return

    await call.message.edit_text(
        f"📊 الإحصائيات:\n👥 المستخدمين: {len(get_users())}",
        reply_markup=back
    )


# 👥 المستخدمين
@router.callback_query(lambda c: c.data == "users")
async def users(call: CallbackQuery):

    if call.from_user.id != ADMIN_ID:
        return

    await call.message.edit_text(
        f"👥 عدد المستخدمين: {len(get_users())}",
        reply_markup=back
    )


# 📢 إرسال رسالة
@router.callback_query(lambda c: c.data == "broadcast")
async def broadcast(call: CallbackQuery):

    if call.from_user.id != ADMIN_ID:
        return

    await call.message.edit_text(
        "✍️ اكتب الرسالة الآن",
        reply_markup=back
    )

    @router.message()
    async def send_all(message: types.Message):

        if message.from_user.id != ADMIN_ID:
            return

        users = get_users()

        sent = 0
        for u in users:
            try:
                await message.bot.send_message(u, message.text)
                sent += 1
            except:
                pass

        await message.answer(f"✅ تم الإرسال إلى {sent} مستخدم")


# ⚙️ إعدادات
@router.callback_query(lambda c: c.data == "settings")
async def settings(call: CallbackQuery):

    if call.from_user.id != ADMIN_ID:
        return

    await call.message.edit_text(
        "⚙️ إعدادات العمدة (قريباً ميزات إضافية)",
        reply_markup=back
    )


# 🔙 رجوع
@router.callback_query(lambda c: c.data == "back")
async def back_menu(call: CallbackQuery):

    admin_panel = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 الإحصائيات", callback_data="stats")],
        [InlineKeyboardButton(text="📢 إرسال رسالة", callback_data="broadcast")],
        [InlineKeyboardButton(text="👥 المستخدمين", callback_data="users")],
        [InlineKeyboardButton(text="⚙️ إعدادات", callback_data="settings")]
    ])

    await call.message.edit_text(
        "👑 لوحة العمدة:",
        reply_markup=admin_panel
    )
