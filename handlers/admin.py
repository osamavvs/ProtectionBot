from aiogram import Router, types
from aiogram.types import CallbackQuery

from db import get_users
from config import ADMIN_ID

router = Router()


# 📢 زر إرسال رسالة
@router.callback_query(lambda c: c.data == "send")
async def send_menu(call: CallbackQuery):
    if call.from_user.id != ADMIN_ID:
        return

    await call.message.answer("✍️ اكتب الرسالة الآن لإرسالها للجميع")


# 👥 عدد المستخدمين
@router.callback_query(lambda c: c.data == "users")
async def users_count(call: CallbackQuery):
    if call.from_user.id != ADMIN_ID:
        return

    users = get_users()
    await call.message.answer(f"👥 عدد المستخدمين: {len(users)}")


# 🚫 حظر (نخليه لاحقاً)
@router.callback_query(lambda c: c.data == "ban")
async def ban_user(call: CallbackQuery):
    if call.from_user.id != ADMIN_ID:
        return

    await call.message.answer("🚫 ميزة الحظر سيتم إضافتها لاحقاً")
