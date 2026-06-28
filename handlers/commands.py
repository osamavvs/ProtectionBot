from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("مرحباً بك في بوت الحماية الخارق! أنا جاهز لحماية مجموعتك.")
