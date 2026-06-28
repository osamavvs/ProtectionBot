from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

router = Router()

# تعريف معرف الأدمن الخاص بك
ADMIN_ID = 8074717568

@router.message(Command("start"))
async def cmd_start(message: Message):
    # التحقق مما إذا كان المستخدم هو الأدمن
    if message.from_user.id == ADMIN_ID:
        # إنشاء لوحة التحكم (الأزرار)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="قفل المجموعة 🔒", callback_data="lock_group")],
            [InlineKeyboardButton(text="إحصائيات 📊", callback_data="stats")]
        ])
        await message.answer("🛠 **أهلاً بك يا أدمن، هذه لوحة التحكم الخاصة بك:**", reply_markup=keyboard)
    else:
        # الرسالة التي تظهر للمستخدمين العاديين
        await message.answer("مرحباً بك في بوت الحماية الخارق! أنا جاهز لحماية مجموعتك.")
