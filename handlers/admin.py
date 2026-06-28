from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("تفعيل"))
async def activate_bot(message: types.Message):
    # هنا تضع كود إضافة المجموعة لقاعدة البيانات
    await message.answer("تم تفعيل البوت في هذه المجموعة بنجاح!")
