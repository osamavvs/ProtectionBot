from aiogram.types import Message
from aiogram.filters import Command

# دالة للتحقق من أن المستخدم مشرف
async def is_admin(message: Message):
    member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in ['creator', 'administrator']

@router.message(F.text == "قفل الروابط")
async def lock_links_command(message: Message):
    if await is_admin(message):
        await set_links_lock(message.chat.id, 1)
        await message.answer("تم تفعيل القفل للمشرفين.")
    else:
        await message.answer("عذراً، هذا الأمر للمشرفين فقط.")
