from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart

router = Router()

# هذا الفلتر (F.chat.type == "private") يضمن أن الأمر لا يعمل نهائياً داخل المجموعات
@router.message(F.chat.type == "private", CommandStart())
async def send_private_start(message: Message):
    
    # التحقق من أن المستخدم هو المطور أسامة فقط
    if message.from_user.username != "U_K44":
        await message.reply("🚸 عذراً عزيزي، سورس كرستال مخصص للمجموعات فقط!\n👑 مطور السورس: @U_K44")
        return

    start_text = """👑 أهلاً أدمن كرستال
    
💎 أهلاً بك في Crystal Bot

✨ نظام متكامل للإدارة والتحكم
⚡ سرعة + حماية + أدوات قوية

🔷 اختر من الأزرار بالأسفل"""

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 الإحصائيات", callback_data="stats")],
        [InlineKeyboardButton(text="📢 إرسال رسالة", callback_data="send_msg")],
        [InlineKeyboardButton(text="👥 المستخدمين", callback_data="users_list")]
    ])
    
    await message.reply(text=start_text, reply_markup=keyboard)
