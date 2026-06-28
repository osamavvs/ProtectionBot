from db import add_user
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "🛡 أهلاً بك في بوت الحماية.\n\n"
        "تم تشغيل البوت بنجاح."
    )
