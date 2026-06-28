from aiogram import Router, F, types
from database import set_links_lock

router = Router()

# الأمر بدون سلاش
@router.message(F.text == "قفل الروابط")
async def lock_links_command(message: types.Message):
    await set_links_lock(message.chat.id, 1)
    await message.answer("تم تفعيل قفل الروابط.")

# الأمر بدون سلاش
@router.message(F.text == "فتح الروابط")
async def unlock_links_command(message: types.Message):
    await set_links_lock(message.chat.id, 0)
    await message.answer("تم إلغاء تفعيل قفل الروابط.")
