from aiogram import Router, F
from aiogram.types import Message, ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
import random

# تعريف الراوتر بشكل صحيح لتجنب خطأ الـ NameError
router = Router()

# قاعدة بيانات مؤقتة لحفظ أقفال وإعدادات القروبات
group_settings = {}

def get_settings(chat_id):
    if chat_id not in group_settings:
        group_settings[chat_id] = {
            "links": False,     
            "forward": False,   
            "username": False   
        }
    return group_settings[chat_id]

# فحص رتبة المشرف
async def is_admin(message: Message) -> bool:
    if message.chat.type == "private":
        return False
    member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    return member.status in ["creator", "administrator"]

# --- 1. حظر الخاص لـ سورس كرستال ---
@router.message(F.chat.type == "private")
async def block_private(message: Message):
    private_text = """🚸 **عذراً عزيزي، سورس كرستال مخصص للمجموعات فقط!**

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
    await message.reply(f"📌 المجموعه » {message.chat.title}\n✨ تم تفعيلها بنجاح في سورس كرستال.")

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

@router.message(F.chat.type.in_({"group", "supergroup"}), F.text == "قفل التوجيه")
async def lock_forward(message: Message):
    if not await is_admin(message): return
    get_settings(message.chat.id)["forward"] = False
    await message.reply("🔒 تم قفل التوجيه، سيتم حذف أي رسالة موجهة.")

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

# --- 3. دالة عرض القائمة الرئيسية للأوامر بالأزرار الشفافة لـ سورس كرستال ---
@router.message(F.chat.type.in_({"group", "supergroup"}), F.text == "الاوامر")
async def send_group_commands(message: Message):
    if not await is_admin(message): return
    
    main_text = """✧ ¦ اوامـر الـبـوت الـرئـيـسـيـة
— — — — — — — — — —
✧ ¦ م1 ← اوامر الحمايه
✧ ¦ م2 ← اوامر الادمنيه
✧ ¦ م3 ← اوامر المدراء
✧ ¦ م4 ← اوامر المنشئين
✧ ¦ م5 ← اوامر المالكين
✧ ¦ م6 ← اوامر التحشيش
✧ ¦ م7 ← اوامر المطور
✧ ¦ م8 ← اوامر التسليه
✧ ¦ م9 ← اوامر البنك"""

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="{ 2 }", callback_data="cmd_2"),
            InlineKeyboardButton(text="{ 1 }", callback_data="cmd_1")
        ],
        [
            InlineKeyboardButton(text="{ 4 }", callback_data="cmd_4"),
            InlineKeyboardButton(text="{ 3 }", callback_data="cmd_3")
        ],
        [
            InlineKeyboardButton(text="{ 6 }", callback_data="cmd_6"),
            InlineKeyboardButton(text="{ 5 }", callback_data="cmd_5")
        ],
        [
            InlineKeyboardButton(text="{ الالعاب }", callback_data="cmd_games"),
            InlineKeyboardButton(text="{ م7 }", callback_data="cmd_7")
        ],
        [
            InlineKeyboardButton(text="{ اوامر البنك }", callback_data="cmd_bank"),
            InlineKeyboardButton(text="{ اوامر التسليه }", callback_data="cmd_8")
        ],
        [
            InlineKeyboardButton(text="{ التعطيل / التفعيل }", callback_data="cmd_toggle"),
            InlineKeyboardButton(text="{ القفل / الفتح }", callback_data="cmd_locks")
        ],
        [
            InlineKeyboardButton(text="- قناة السورس .", url="https://t.me/YourChannel")
        ]
    ])
    
    await message.reply(text=main_text, reply_markup=keyboard)

# --- 4. معالجة رسائل الحماية والإدارة والتسلية ---
@router.message(F.chat.type.in_({"group", "supergroup"}))
async def handle_crystal_source(message: Message):
    if not message.text: return
    text = message.text.strip()
    
    if await is_admin(message) and message.reply_to_message:
        target_user = message.reply_to_message.from_user
        
        if text in ["طرد", "حظر"]:
            try:
                await message.chat.ban(user_id=target_user.id)
                await message.reply(f"👤 العضو » {target_user.first_name}\n📌 تم حظره وطرده بنجاح.")
            except: pass
            return
        elif text in ["الغاء الحظر", "الغاء طرد"]:
            try:
                await message.chat.unban(user_id=target_user.id)
                await message.reply(f"👤 العضو » {target_user.first_name}\n📌 تم إلغاء حظره.")
            except: pass
            return
        elif text == "كتم":
            try:
                await message.chat.restrict(user_id=target_user.id, permissions=ChatPermissions(can_send_messages=False))
                await message.reply(f"🔇 العضو » {target_user.first_name}\n📌 تم كتمه.")
            except: pass
            return
        elif text == "الغاء الكتم":
            try:
                await message.chat.restrict(user_id=target_user.id, permissions=ChatPermissions(can_send_messages=True, can_send_photos=True, can_send_videos=True, can_send_audios=True, can_send_other_messages=True))
                await message.reply(f"🔊 العضو » {target_user.first_name}\n📌 تم إلغاء كتمه.")
            except: pass
            return

    if not await is_admin(message):
        settings = get_settings(message.chat.id)
        if not settings["links"] and ("http" in text or "t.me/" in text or ".com" in text):
            try: return await message.delete()
            except: pass
        if not settings["forward"] and message.forward_date:
            try: return await message.delete()
            except: pass
        if not settings["username"] and "@" in text:
            try: return await message.delete()
            except: pass

    if text == "ايدي":
        await message.reply(f"🆔 ايديك » `{message.from_user.id}`\n🗂️ ايدي الكروب » `{message.chat.id}`")
    elif text == "اسمي":
        await message.reply(f"👤 اسمك الحركي » {message.from_user.first_name}")
    elif text == "رتبتي":
        role = "مشرف المجموعة 😎" if await is_admin(message) else "عضو محترم ✨"
        await message.reply(f"🎖️ رتبتك داخل المجموعة » {role}")
    elif text == "كشف" and message.reply_to_message:
        tgt = message.reply_to_message.from_user
        await message.reply(f"📋 معلومات العضو:\n• الاسم: {tgt.full_name}\n• الايدي: `{tgt.id}`")
    elif text == "هلو":
        await message.reply(f"هلا عيني {message.from_user.first_name}، نورت سورس كرستال 💎")
