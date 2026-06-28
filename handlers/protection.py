from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

# سنستخدم متغيرًا مؤقتًا الآن، ثم لاحقًا سننقله إلى قاعدة البيانات
links_locked = False

@router.message(Command("lock_links"))
async def lock_links(message: Message):
    global links_locked
    links_locked = True
    await message.answer("🔒 تم قفل الروابط.")

@router.message(Command("unlock_links"))
async def unlock_links(message: Message):
    global links_locked
    links_locked = False
    await message.answer("🔓 تم فتح الروابط.")

@router.message()
async def check_links(message: Message):
    if not links_locked:
        return

    text = message.text or ""
    if "http://" in text or "https://" in text or "t.me/" in text:
        await message.delete()
