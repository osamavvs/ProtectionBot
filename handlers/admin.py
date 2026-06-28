from aiogram import Router, F
from aiogram.types import Message, ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import random

router = Router()

# قاعدة بيانات مؤقتة لحفظ إعدادات القروبات (الروابط)
group_settings = {}

def get_settings(chat_id):
    if chat_id not in group_settings:
        group_settings[chat_id] = {
            "links": False,  # مقفول تلقائياً لحماية المجموعة
        }
    return group_settings[chat_id]

# دالة مساعدة للتحقق من رتبة الأدمن
async def is_admin(message: Message) -> bool:
    if message.chat.type == "private":
        return True
    member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    return member.status in ["creator", "administrator"]

# --- 1. لوحة الخاص (سورس كرستال) ---
@router.message(F.chat.type == "private", F.text == "الاوامر")
async def send_private_panel(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="طريقة التفعيل 🛠️", callback_data="help_activate")]
    ])
    
    panel_text = """💎 **أهلاً بك في لوحة تحكم سورس كرستال للحماية.**

• البوت مبرمج لإدارة وحماية مجموعتك تلقائياً وبأعلى سرعة.
• جميع الأوامر داخل القروبات تعمل بالرد المباشر وبدون الشارطة (/)."""
    
    await message.reply(text=panel_text, reply_markup=keyboard)

@router.callback_query(F.data == "help_activate")
async def help_callback(call: CallbackQuery):
    help_text = """🛠️ **طريقة تفعيل البوت داخل القروب:**

1️⃣ قم بإضافة البوت إلى قروبك.
2️⃣ ارفع البوت مشرف (أدمن) واعطه صلاحية الحذف والحظر.
3️⃣ أرسل كلمة `تفعيل` داخل القروب ليتم ربطه بنجاح."""
    
    await call.message.edit_text(
        text=help_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="رجوع 🔙", callback_data="back_to_main")]])
    )

@router.callback_query(F.data == "back_to_main")
async def back_callback(call: CallbackQuery):
    main_text = """💎 **أهلاً بك في لوحة تحكم سورس كرستال للحماية.**

• جميع الأوامر داخل القروبات تعمل بالرد المباشر وبدون الشارطة (/)."""
    
    await call.message.edit_text(
        text=main_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="طريقة التفعيل 🛠️", callback_data="help_activate")]])
    )

# --- 2. أوامر المجموعات والردود الذكية والتسلية ---

@router.message(F.chat.type.in_({"group", "supergroup"}), F.text == "تفعيل")
async def activate_group(message: Message):
    if not await is_admin(message): return
    get_settings(message.chat.id)
    await message.reply(f"📌 Mجموعه » {message.chat.title}\n💎 تم تفعيلها بنجاح في سورس كرستال.")

@router.message(F.chat.type.in_({"group", "supergroup"}), F.text == "قفل الروابط")
async def lock_links(message: Message):
    if not await is_admin(message): return
    get_settings(message.chat.id)["links"] = False
    await message.reply("🔒 تم قفل الروابط بنجاح، سيتم حذف أي رابط ينشر.")

@router.message(F.chat.type.in_({"group", "supergroup"}), F.text == "فتح الروابط")
async def unlock_links(message: Message):
    if not await is_admin(message): return
    get_settings(message.chat.id)["links"] = True
    await message.reply("🔓 تم فتح الروابط، بإمكان الأعضاء النشر الآن.")

# معالجة كافة الرسائل داخل المجموعات (حماية + ردود + ألعاب)
@router.message(F.chat.type.in_({"group", "supergroup"}))
async def handle_group_messages(message: Message):
    if not message.text: return
    
    # [أولاً] أوامر المشرفين بالرد السريع
    if await is_admin(message) and message.reply_to_message:
        if message.text == "طرد":
            try:
                await message.chat.ban(user_id=message.reply_to_message.from_user.id)
                await message.reply(f"👤 العضو » {message.reply_to_message.from_user.first_name}\n📌 تم طرده من المجموعه بنجاح.")
            except: pass
            return

        elif message.text == "كتم":
            try:
                await message.chat.restrict(user_id=message.reply_to_message.from_user.id, permissions=ChatPermissions(can_send_messages=False))
                await message.reply(f"🔇 العضو » {message.reply_to_message.from_user.first_name}\n📌 تم كتمه وتوجيه عقوبة الصمت له.")
            except: pass
            return

        elif message.text == "الغاء الكتم":
            try:
                await message.chat.restrict(user_id=message.reply_to_message.from_user.id, permissions=ChatPermissions(can_send_messages=True, can_send_photos=True, can_send_videos=True, can_send_audios=True))
                await message.reply(f"🔊 العضو » {message.reply_to_message.from_user.first_name}\n📌 تم إلغاء كتمه وبإمكانه التحدث الآن.")
            except: pass
            return

    # [ثانياً] الحماية التلقائية من الروابط للأعضاء العاديين
    if not await is_admin(message):
        settings = get_settings(message.chat.id)
        if not settings["links"] and ("http" in message.text or "t.me/" in message.text or ".com" in message.text):
            try: 
                await message.delete()
            except: pass
            return

    # [ثالثاً] قسم الردود العامة والتسلية (بدون /) لكل الأعضاء
    text = message.text.strip()
    
    # الردود التفاعلية
    if text == "هلو":
        await message.reply(f"هلا عيني {message.from_user.first_name}، نورت القروب 💎")
    elif text == "البوت شغال؟":
        await message.reply("شغال وعال العال، سورس كرستال بخدمتكم! 😎")
    elif text == "شلونكم":
        await message.reply("الحمد لله بخير، أنت شلونك عساك طيب؟ ✨")
        
    # ألعاب تسلية سريعة
    elif text == "نسبة حبه":
        if message.reply_to_message:
            num = random.randint(0, 100)
            await message.reply(f"❤️ نسبة حبك لـ {message.reply_to_message.from_user.first_name} هي: {num}% 💎")
        else:
            await message.reply("قم بالرد على الشخص لمعرفة نسبة حبك له!")
    elif text == "حظي":
        quotes = [
            "حظك اليوم يجنن ومبشر بخير! ✨", 
            "اليوم حظك نص ونص، دير بالك 🦦", 
            "حظك اليوم عالي وتوب التوب! 🚀", 
            "اممم، يحتاج تبتسم حتى يتعدل حظك 😇"
        ]
        await message.reply(f"🔮 {message.from_user.first_name}، {random.choice(quotes)}")
