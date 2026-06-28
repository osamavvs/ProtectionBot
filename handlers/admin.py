from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database import set_links_lock

router = Router()

# دالة التحقق من المشرفين
async def is_admin(message: types.Message):
    member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in ['creator', 'administrator']

# لوحة التحكم
def get_admin_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="قفل الروابط"), KeyboardButton(text="فتح الروابط")],
        [KeyboardButton(text="قفل الصور"), KeyboardButton(text="فتح الصور")]
    ], resize_keyboard=True)

# أمر إظهار لوحة التحكم
@router.message(F.text == "الاوامر")
async def show_commands(message: types.Message):
    if await is_admin(message):
        await message.answer("أهلاً بك يا مطور، هذه لوحة التحكم:", reply_markup=get_admin_keyboard())
    else:
        await message.answer("عذراً، هذا الأمر للمشرفين فقط.")

# أوامر التحكم بالقفل
@router.message(F.text == "قفل الروابط")
async def lock_links(message: types.Message):
    if await is_admin(message):
        await set_links_lock(message.chat.id, 1)
        await message.answer("تم تفعيل قفل الروابط.")

@router.message(F.text == "فتح الروابط")
async def unlock_links(message: types.Message):
    if await is_admin(message):
        await set_links_lock(message.chat.id, 0)
        await message.answer("تم إلغاء تفعيل قفل الروابط.")
