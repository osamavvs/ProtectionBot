from aiogram import Router, F, types
from aiogram.filters import Command

router = Router()

# هنا نضع منطق القفل والفتح
# مثال: قفل الروابط
@router.message(F.text.contains("http"))
async def lock_links(message: types.Message):
    # نتحقق إذا كانت المجموعة مفعلة (سنربطها بقاعدة البيانات لاحقاً)
    # حالياً كود تجريبي للحماية
    await message.delete()
    await message.answer(f"عذراً {message.from_user.first_name}، يمنع إرسال الروابط في هذه المجموعة!")

# مثال: قفل الصور
@router.message(F.content_type == "photo")
async def lock_photos(message: types.Message):
    await message.delete()
    await message.answer("يمنع إرسال الصور هنا!")
