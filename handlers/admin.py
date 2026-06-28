from aiogram import Router, F
from aiogram.types import Message, ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

router = Router()

# قاعدة بيانات مؤقتة في الذاكرة لحفظ إعدادات القروبات (الروابط، التوجيه)
group_settings = {}

def get_settings(chat_id):
    if chat_id not in group_settings:
        group_settings[chat_id] = {
            "links": False,  # False يعني مقفول تلقائياً (يتم حذف الروابط)
        }
    return group_settings[chat_id]

# دالة مساعدة للتأكد إذا كان الشخص مشرف
async def is_admin(message: Message) -> bool:
    if message.chat.type == "private":
        return True
    member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    return member.status in ["creator", "administrator"]

# --- 1. لوحة التحكم بالخاص (أزرار شفافة) ---
@router.message(F.chat.type == "private", F.text == "الاوامر")
async def send_private_panel(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="طريقة التفعيل 🛠️", callback_data="help_activate")]
    ])
    
    await message.reply(
        "💎 **أهلاً بك في لوحة تحكم سورس كرستال للحماية.**\n\n"
        "• البوت مبرمج لإدارة وحماية مجموعتك تلقائياً وبأعلى سرعة.\n"
        "• جميع الأوامر داخل القروبات تعمل بالرد المباشر وبدون الشارطة (/).",
        reply_markup=keyboard
    )

@router.callback_query(F.data == "help_activate")
async def help_callback(call: CallbackQuery):
    await call.message.edit_text(
        "🛠️ **طريقة تفعيل البوت داخل القروب:**
