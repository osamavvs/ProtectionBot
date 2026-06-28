from aiogram import Router, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import set_links_lock

router = Router()

# دالة التحقق من المشرفين
async def is_admin(message: types.Message):
    member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in ['creator', 'administrator']

# تعريف الأزرار الشفافة (Inline)
def get_inline_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="قفل الروابط", callback_data="lock_links"), 
         InlineKeyboardButton(text="فتح الروابط", callback_data="unlock_links")]
    ])

# أمر إظهار الأزرار
@router.message(F.text == "الاوامر")
async def show_commands(message: types.Message):
    if await is_admin(message):
        await message.answer("لوحة التحكم الشفافة:", reply_markup=get_inline_keyboard())

# معالجة الضغط على الأزرار (Callback)
@router.callback_query(F.data.in_(["lock_links", "unlock_links"]))
async def handle_callback(callback: types.CallbackQuery):
    if callback.data == "lock_links":
        await set_links_lock(callback.message.chat.id, 1)
        await callback.answer("تم قفل الروابط!")
    elif callback.data == "unlock_links":
        await set_links_lock(callback.message.chat.id, 0)
        await callback.answer("تم فتح الروابط!")
