from aiogram import Router, F
from aiogram.types import Message, ChatPermissions
import random

router = Router()

# قاعدة بيانات مؤقتة لحفظ أقفال وإعدادات القروبات
group_settings = {}

def get_settings(chat_id):
    if chat_id not in group_settings:
        group_settings[chat_id] = {
            "links": False,     # مقفول تلقائياً
            "forward": False,   # مقفول تلقائياً
            "username": False   # مقفول تلقائياً
        }
    return group_settings[chat_id]

# فحص رتبة المشرف
async def is_admin(message: Message) -> bool:
    if message.chat.type == "private":
        return False
    member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    return member.status in ["creator", "administrator"]

# --- 1. حظر الخاص تماماً نفس أسلوب تشاكي ---
@router.message(F.chat.type == "private")
async def block_private(message: Message):
    private_text = """🚸 **عذراً عزيزي، سورس تشاكي مخصص للمجموعات فقط!**

❌ لا يمكنك استخدام أوامر البوت هنا في الخاص.
💎 أضف البوت إلى مجموعتك وارفعها مشرفاً لتستمتع بالحماية والتسلية."""
    try:
        await message.reply(text=private_text)
    except: pass

# --- 2. أوامر التفعيل والتحكم والأقفال للقروب ---

@router.message(F.chat.type.in_({"group", "supergroup"}), F.text == "تفعيل")
async def activate_group(message: Message):
    if not await is_admin(message): return
    get_settings(message.chat.id)
    await message.reply(f"📌 المجموعه » {message.chat.title}\n✨ تم تفعيلها بنجاح في سورس تشاكي.")

# قفل وفتح الروابط
@router.message(F.chat.type.in_({"group", "supergroup"}), F.text == "قفل الروابط")
async def lock_links(message: Message):
    if not await is_admin(message): return
    get_settings(message.chat.id)["links"] = False
    await message.reply("🔒 تم قفل الروابط بنجاح، سيتم تنظيف المجموعة تلقائياً.")

@router.message(F.chat.type.in_({"group", "supergroup"}), F.text == "فتح الروابط")
async def unlock_links(message: Message):
    if not await is_admin(message): return
    get_settings(message.chat.id)["links"] = True
    await message.reply("🔓 تم فتح الروابط، بإمكان الأعضاء النشر الآن.")

# قفل وفتح التوجيه (Forward)
@router.message(F.chat.type.in_({"group", "supergroup"}), F.text == "قفل التوجيه")
async def lock_forward(message: Message):
    if not await is_admin(message): return
    get_settings(message.chat.id)["forward"] = False
    await message.reply("🔒 تم قفل التوجيه، سيتم حذف أي رسالة موجهة.")

@router.message(F.chat.type.in_({"group", "supergroup"}), F.text == "فتح التوجيه")
async def unlock_forward(message: Message):
    if not await is_admin(message): return
    get_settings(message.chat.id)["forward"] = True
    await message.reply("🔓 تم فتح التوجيه بنجاح.")

# قفل وفتح المعرفات (@)
@router.message(F.chat.type.in_({"group", "supergroup"}), F.text == "قفل المعرفات")
async def lock_usernames(message: Message):
    if not await is_admin(message): return
    get_settings(message.chat.id)["username"] = False
    await message.reply("🔒 تم قفل المعرفات، سيتم حذف أي معرف ينشر.")

@router.message(F.chat.type.in_({"group", "supergroup"}), F.text == "فتح المعرفات")
async def unlock_usernames(message: Message):
    if not await is_admin(message): return
    get_settings(message.chat.id)["username"] = True
    await message.reply("🔓 تم فتح المعرفات بنجاح.")

# --- 3. معالجة كافة رسائل وحماية وألعاب المجموعة ---
@router.message(F.chat.type.in_({"group", "supergroup"}))
async def handle_chucky_source(message: Message):
    if not message.text: return
    text = message.text.strip()
    
    # [أولاً] أوامر المشرفين بالرد السريع (نظام تشاكي الحاسم)
    if await is_admin(message) and message.reply_to_message:
        target_user = message.reply_to_message.from_user
        
        if text in ["طرد", "حظر"]:
            try:
                await message.chat.ban(user_id=target_user.id)
                await message.reply(f"👤 العضو » {target_user.first_name}\n📌 تم حظره وطرده من المجموعة بنجاح.")
            except: pass
            return

        elif text in ["الغاء الحظر", "الغاء طرد"]:
            try:
                await message.chat.unban(user_id=target_user.id)
                await message.reply(f"👤 العضو » {target_user.first_name}\n📌 تم إلغاء حظره ويمكنه الدخول الآن.")
            except: pass
            return

        elif text == "كتم":
            try:
                await message.chat.restrict(user_id=target_user.id, permissions=ChatPermissions(can_send_messages=False))
                await message.reply(f"🔇 العضو » {target_user.first_name}\n📌 تم تقييده وتوجيه عقوبة الصمت له.")
            except: pass
            return

        elif text == "الغاء الكتم":
            try:
                await message.chat.restrict(user_id=target_user.id, permissions=ChatPermissions(can_send_messages=True, can_send_photos=True, can_send_videos=True, can_send_audios=True, can_send_other_messages=True))
                await message.reply(f"🔊 العضو » {target_user.first_name}\n📌 تم فك كتمه وبإمكانه التحدث الآن.")
            except: pass
            return

    # [ثانياً] الحماية التلقائية للأعضاء العاديين (الفحص الذكي)
    if not await is_admin(message):
        settings = get_settings(message.chat.id)
        
        # فحص الروابط
        if not settings["links"] and ("http" in text or "t.me/" in text or ".com" in text):
            try: return await message.delete()
            except: pass
            
        # فحص التوجيه
        if not settings["forward"] and message.forward_date:
            try: return await message.delete()
            except: pass
            
        # am فحص المعرفات
        if not settings["username"] and "@" in text:
            try: return await message.delete()
            except: pass

    # [ثالثاً] أوامر معلومات الأعضاء (سورس تشاكي)
    if text == "ايدي":
        await message.reply(f"🆔 ايديك » `{message.from_user.id}`\n🗂️ ايدي الكروب » `{message.chat.id}`")
    elif text == "اسمي":
        await message.reply(f"👤 اسمك الحركي » {message.from_user.first_name}")
    elif text == "رتبتي":
        role = "مشرف المجموعة 😎" if await is_admin(message) else "عضو محترم ✨"
        await message.reply(f"🎖️ رتبتك داخل المجموعة » {role}")
    elif text == "كشف" and message.reply_to_message:
        tgt = message.reply_to_message.from_user
        await message.reply(f"📋 معلومات العضو:\n• الاسم: {tgt.full_name}\n• الايدي: `{tgt.id}`\n• اليوزر: @{tgt.username if tgt.username else 'لا يوجد'}")
    elif text == "الرابط":
        try:
            link = await message.chat.export_invite_link()
            await message.reply(f"🔗 رابط المجموعة الخاص بسورس تشاكي:\n{link}")
        except:
            await message.reply("❌ البوت يحتاج إلى صلاحية إدارة الروابط لاستخراج الرابط.")

    # [رابعاً] قسم التسلية والردود السريعة
    elif text == "هلو":
        await message.reply(f"هلا عيني {message.from_user.first_name}، نورت سورس تشاكي 💎")
    elif text == "البوت شغال؟":
        await message.reply("شغال طيارة وعال العال! ⚡")
    elif text == "نسبة حبه":
        if message.reply_to_message:
            await message.reply(f"❤️ نسبة حبك لـ {message.reply_to_message.from_user.first_name} هي: {random.randint(0, 100)}% 💎")
        else:
            await message.reply("سوي رد على الشخص أولاً!")
    elif text == "حظي":
        quotes = ["حظك يجنن اليوم ومبشر بخير! ✨", "حظك تعبان اليوم روح نام أحسن 🦦", "حظك عالي وتوب التوب! 🚀"]
        await message.reply(f"🔮 {message.from_user.first_name}، {random.choice(quotes)}")
    elif text == "تويت":
        tweets = ["لا تبرر لأحد، اتركهم يفهمونك خطأ ويريحونك من لغوتهم.", "أحياناً العزلة أحلى من مئة صديق منافق.", "كن عظيماً ولا ترضى بأقل مما تستحق."]
        await message.reply(f"🐦 تـويـت تشاكي: {random.choice(tweets)}")
    elif text == "كول":
        sayings = ["من حفر حفرة لأخيه وقع فيها.", "الصمت حكمه وقليل فاعله.", "الوقت كالسيف إن لم تقطعه قطعك."]
        await message.reply(f"💬 كول المأثور: {random.choice(sayings)}")
