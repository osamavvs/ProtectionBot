from aiogram import Router, F
from aiogram.types import Message, ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# قاعدة بيانات مؤقتة لحفظ حالات القفل لكل قروب
group_settings = {}

def get_settings(chat_id):
    if chat_id not in group_settings:
        # افتراضياً كل الحمايات مفتوحة (True تعني مسموح، False تعني مقفول)
        group_settings[chat_id] = {
            "الكل": True, "الدخول": True, "الروابط": True, "المعرف": True,
            "التاك": True, "الشارحه": True, "التعديل": True, "تعديل الميديا": True,
            "المتحركه": True, "الملفات": True, "الصور": True, "الفيديو": True,
            "الستوري": True, "الماركدوان": True, "البوتات": True, "التكرار": True,
            "الكلايش": True, "السيلفي": True, "الملصقات": True, "الانلاين": True,
            "الدردشه": True, "التوجيه": True, "الاغاني": True, "الصوت": True,
            "الجهات": True, "الاشعارات": True, "التثبيت": True, "الوسائط": True,
            "التفليش": True, "وسائط المميزين": True, "الفشار": True, "ارسال القناة": True,
            "القنوات": True, "الإنكليزيه": True, "الفارسيه": True, "الكفر": True, "الاباحي": True
        }
    return group_settings[chat_id]

async def is_admin(message: Message) -> bool:
    if message.chat.type == "private":
        return False
    member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    return member.status in ["creator", "administrator"]

# --- 1. أوامر التفعيل والتعطيل للقروب ---
@router.message(F.chat.type.in_({"group", "supergroup"}), F.text == "تفعيل")
async def activate_group(message: Message):
    if not await is_admin(message): return
    get_settings(message.chat.id)
    await message.reply(f"📌 المجموعه » {message.chat.title}\n✨ تم تفعيلها بنجاح في سورس كرستال.")

# --- 2. معالجة أوامر القفل والفتح ديناميكياً ---
@router.message(F.chat.type.in_({"group", "supergroup"}), lambda msg: msg.text and (msg.text.startswith("قفل ") or msg.text.startswith("فتح ")))
async def handle_locks_and_unlocks(message: Message):
    if not await is_admin(message): return
    
    parts = message.text.strip().split(" ", 1)
    action = parts[0]  # "قفل" أو "فتح"
    target = parts[1]  # الأمر المراد قفله (مثل "الروابط"، "المعرف")
    
    settings = get_settings(message.chat.id)
    
    if target in settings:
        if action == "قفل":
            settings[target] = False
            await message.reply(f"🔒 تم قفل **{target}** بنجاح.")
        else:
            settings[target] = True
            await message.reply(f"🔓 تم فتح **{target}** بنجاح.")
    else:
        # إذا لم يكن الأمر مسجلاً في القائمة الافتراضية
        pass

# --- 3. دالة عرض القائمة الرئيسية للأوامر بالأزرار الشفافة ---
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
        [[InlineKeyboardButton(text="{ 2 }", callback_data="cmd_2"), InlineKeyboardButton(text="{ 1 }", callback_data="cmd_1")]],
        [[InlineKeyboardButton(text="{ 4 }", callback_data="cmd_4"), InlineKeyboardButton(text="{ 3 }", callback_data="cmd_3")]],
        [[InlineKeyboardButton(text="{ 6 }", callback_data="cmd_6"), InlineKeyboardButton(text="{ 5 }", callback_data="cmd_5")]],
        [[InlineKeyboardButton(text="{ الالعاب }", callback_data="cmd_games"), InlineKeyboardButton(text="{ م7 }", callback_data="cmd_7")]],
        [[InlineKeyboardButton(text="{ اوامر البنك }", callback_data="cmd_bank"), InlineKeyboardButton(text="{ اوامر التسليه }", callback_data="cmd_8")]],
        [[InlineKeyboardButton(text="{ التعطيل / التفعيل }", callback_data="cmd_toggle"), InlineKeyboardButton(text="{ القفل / الفتح }", callback_data="cmd_locks")]],
        [[InlineKeyboardButton(text="- قناة السورس .", url="https://t.me/BBABB9")]]
    ])
    
    await message.reply(text=main_text, reply_markup=keyboard)

# --- 4. فحص وحذف الرسائل المقفولة للأعضاء العاديين ---
@router.message(F.chat.type.in_({"group", "supergroup"}))
async def monitor_group_messages(message: Message):
    if not message.text: return
    text = message.text.strip()
    
    if text.startswith("/start") or text == "الاوامر": return
    if await is_admin(message): return  # المشرفين لا ينطبق عليهم القفل
    
    settings = get_settings(message.chat.id)
    
    # 1. فحص حماية الروابط
    if not settings["الروابط"] and ("http" in text or "t.me/" in text or ".com" in text):
        try: return await message.delete()
        except: pass
        
    # 2. فحص حماية المعرفات
    if not settings["المعرف"] and "@" in text:
        try: return await message.delete()
        except: pass

    # 3. فحص التوجيه (Forward)
    if not settings["التوجيه"] and message.forward_date:
        try: return await message.delete()
        except: pass

    # 4. أوامر الحظر والكتم اليدوي بالإرسال
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user
        if text in ["طرد", "حظر"]:
            try: await message.chat.ban(user_id=target_user.id)
            except: pass
        elif text == "كتم":
            try: await message.chat.restrict(user_id=target_user.id, permissions=ChatPermissions(can_send_messages=False))
            except: pass

    # الميزات الباقية (مثل الأيدي والاسم)
    if text == "ايدي":
        await message.reply(f"🆔 ايديك » `{message.from_user.id}`\n🗂️ ايدي الكروب » `{message.chat.id}`")
    elif text == "اسمي":
        await message.reply(f"👤 اسمك الحركي » {message.from_user.first_name}")
    elif text == "مطور" or text == "المطور":
        await message.reply("👑 مطور السورس الغالي هو: @U_K44")
