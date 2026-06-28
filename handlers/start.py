from aiogram import Router, types
from aiogram.filters import CommandStart

from db import add_user

router = Router()

@router.message(CommandStart())
async def start(message: types.Message):
    # تسجيل المستخدم
    add_user(message.from_user.id)

    await message.answer(
        "👋 أهلاً بيك!\nالبوت شغال بنجاح 🔥"
    )
