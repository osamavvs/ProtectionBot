from aiogram import Router, F, types
from database import is_links_locked # استيراد الفحص

router = Router()

@router.message(F.text.contains("http"))
async def lock_links(message: types.Message):
    # نتحقق من قاعدة البيانات
    if await is_links_locked(message.chat.id):
        await message.delete()
        await message.answer("تم حذف الرابط لأن القفل مفعل!")
