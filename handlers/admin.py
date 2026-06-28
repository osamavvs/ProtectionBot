from aiogram import Router, types
from aiogram.filters import Command
from database import set_links_lock # استيراد دالة التحديث

router = Router()

@router.message(Command("قفل_الروابط"))
async def lock_links_command(message: types.Message):
    # تفعيل القفل (1 يعني مفعل)
    await set_links_lock(message.chat.id, 1)
    await message.answer("تم تفعيل قفل الروابط في هذه المجموعة.")

@router.message(Command("فتح_الروابط"))
async def unlock_links_command(message: types.Message):
    # تعطيل القفل (0 يعني معطل)
    await set_links_lock(message.chat.id, 0)
    await message.answer("تم إلغاء تفعيل قفل الروابط.")
