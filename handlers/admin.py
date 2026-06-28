from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(F.text == "الاوامر")
async def show_panel(message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="قفل الروابط 🔗", callback_data="lock_links")],
        [InlineKeyboardButton(text="فتح الروابط 🔓", callback_data="unlock_links")]
    ])
    await message.answer("🛠 **لوحة تحكم البوت:**\nاختر من الأزرار بالأسفل:", reply_markup=kb)
