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
        "✨ **أهلاً بك في لوحة تحكم البوت العالمي للحماية.**\n\n"
        "• البوت مبرمج لإدارة وحماية مجموعتك تلقائياً وبأعلى سرعة.\n"
        "• جميع الأوامر داخل القروبات تعمل بالرد المباشر وبدون الشارطة (/).",
        reply_markup=keyboard
    )

@router.callback_query(F.data == "help_activate")
async def help_callback(call: CallbackQuery):
    await call.message.edit_text(
        "🛠️ **طريقة تفعيل البوت داخل القروب:**\n\n"
        "1️⃣ قم بإضافة البوت إلى قروبك.\n"
        "2️⃣ ارفع البوت مشرف (أدمن) واعطه صلاحية الحذف والحظر.\n"
        "3️⃣ أرسل كلمة `تفعيل` داخل القروب ليتم ربطه بنجاح.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="رجوع 🔙", callback_data="back_to_main")]])
    )

@router.callback_query(F.data == "back_to_main")
async def back_callback(call: CallbackQuery):
    await call.message.edit_text(
        "✨ **أهلاً بك في لوحة تحكم البوت العالمي للحماية.**\n\n• جميع الأوامر داخل القروبات تعمل بالرد المباشر وبدون الشارطة (/).",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="طريقة التفعيل 🛠️", callback_data="help_activate")]])
    )

# --- 2. أوامر المجموعات والحماية التلقائية (نفس سورس العمدة) ---

# أمر تفعيل القروب
@router.message(F.chat.type.in_({"group", "supergroup"}), F.text == "تفعيل")
async def activate_group(message: Message):
    if not await is_admin(message):
        return
    get_settings(message.chat.id)
    await message.reply(f"📌 المجموعه » {message.chat.title}\n✨ تم تفعيلها بنجاح في البوت العالمي.")

# أوامر قفل وفتح الروابط بالقروب
@router.message(F.chat.type.in_({"group", "supergroup"}), F.text == "قفل الروابط")
async def lock_links(message: Message):
    if not await is_admin(message):
        return
    settings = get_settings(message.chat.id)
    settings["links"] = False
    await message.reply("🔒 تم قفل الروابط بنجاح، سيتم حذف أي رابط ينشر.")

@router.message(F.chat.type.in_({"group", "supergroup"}), F.text == "فتح الروابط")
async def unlock_links(message: Message):
    if not await is_admin(message):
        return
    settings = get_settings(message.chat.id)
    settings["links"] = True
    await message.reply("🔓 تم فتح الروابط، بإمكان الأعضاء النشر الآن.")

# فحص الرسائل: الحماية والأوامر بالرد
@router.message(F.chat.type.in_({"group", "supergroup"}))
async def handle_group_messages(message: Message):
    # إذا كانت رسالة نصية عادية
    if message.text:
        # 1. تنفيذ أوامر الرد السريع للمشرفين فقط
        if await is_admin(message) and message.reply_to_message:
            
            if message.text == "طرد":
                try:
                    await message.chat.ban(user_id=message.reply_to_message.from_user.id)
                    await message.reply(f"👤 العضو » {message.reply_to_message.from_user.first_name}\n📌 تم طرده من المجموعه بنجاح.")
                except: pass
                return

            elif message.text == "كتم":
                try:
                    permissions = ChatPermissions(can_send_messages=False)
                    await message.chat.restrict(user_id=message.reply_to_message.from_user.id, permissions=permissions)
                    await message.reply(f"🔇 العضو » {message.reply_to_message.from_user.first_name}\n📌 تم كتمه وتوجيه عقوبة الصمت له.")
                except: pass
                return

            elif message.text == "الغاء الكتم":
                try:
                    permissions = ChatPermissions(can_send_messages=True, can_send_photos=True, can_send_videos=True, can_send_audios=True)
                    await message.chat.restrict(user_id=message.reply_to_message.from_user.id, permissions=permissions)
                    await message.reply(f"🔊 العضو » {message.reply_to_message.from_user.first_name}\n📌 تم إلغاء كتمه وبإمكانه التحدث الآن.")
                except: pass
                return

        # 2. الحماية التلقائية من الروابط للأعضاء العاديين
        if not await is_admin(message):
            settings = get_settings(message.chat.id)
            if not settings["links"]:
                if "http" in message.text or "t.me/" in message.text or ".com" in message.text:
                    try:
                        await message.delete()
                    except: pass
