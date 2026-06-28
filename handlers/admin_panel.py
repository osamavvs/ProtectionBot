from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from filters.is_admin import IsAdmin

router = Router()

def get_admin_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="قفل المجموعة 🔒", callback_data="lock_group")],
        [InlineKeyboardButton(text="فتح المجموعة 🔓", callback_data="unlock_group")],
        [InlineKeyboardButton(text="قائمة المحظورين 🚫", callback_data="ban_list")],
        [InlineKeyboardButton(text="الإحصائيات 📊", callback_data="stats")]
    ])
    return keyboard

@router.message(IsAdmin(), Command("start"))
async def admin_start(message: Message):
    await message.answer(
        "🛠 **أهلاً بك يا مدير في لوحة التحكم المركزية**\n"
        "يمكنك التحكم في إعدادات الحماية من هنا:",
        reply_markup=get_admin_keyboard()
    )

@router.message(Command("start"))
async def user_start(message: Message):
    if message.chat.type == "private":
        await message.answer("أهلاً بك في بوت الحماية الخاص بنا. هذا البوت مخصص للمجموعات فقط.")
