from aiogram import Router, types
from aiogram.filters import CommandStart

from db import add_user
from config import ADMIN_ID

router = Router()

@router.message(CommandStart())
async def start(message: types.Message):

    # تسجيل المستخدم
    add_user(message.from_user.id)

    # تمييز الأدمن
    if message.from_user.id == ADMIN_ID:
        await message.answer("👑 أهلاً أدمن\nلوحة التحكم قادمة 🔥")
    else:
        await message.answer("👋 أهلاً بيك\nالبوت شغال بنجاح 🔥")
