from aiogram import Router, F
from aiogram.types import Message, ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

group_settings = {}

def get_settings(chat_id):
    if chat_id not in group_settings:
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
    if message.chat.type == "private": return False
    member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    return member.status in ["creator", "administrator"]

@router.message(F.chat.type.in_({"group", "supergroup"}), F.text == "تفعيل")
async def activate_group(message: Message):
    if not await is_admin(message): return
    get_settings(message.chat.id)
    await message.reply(f"📌 المجموعه » {message.chat.title}\n✨ تم تفعيلها بنجاح في سورس كرستال.")

@router.message(F.chat.type.in_({"group", "supergroup"}), F.text == "الاوامر")
async def send_group_commands(message: Message):
    if not await is_admin(message): return
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="{ 2 }", callback_data="cmd_2"), InlineKeyboardButton(text="{ 1 }", callback_data="cmd_1")],
        [InlineKeyboardButton(text="{ 4 }", callback_data="cmd_4"), InlineKeyboardButton(text="{ 3 }", callback_data="cmd_3")],
        [InlineKeyboardButton(text="{ 6 }", callback_data="cmd_6"), InlineKeyboardButton(text="{ 5 }", callback_data="cmd_5")],
        [InlineKeyboardButton(text="{ الالعاب }", callback_data="cmd_games"), InlineKeyboardButton(text="{ م7 }", callback_data="cmd_7")],
        [InlineKeyboardButton(text="{ اوامر البنك }", callback_data="cmd_bank"), InlineKeyboardButton(text="{ اوامر التسليه }", callback_data="cmd_8")],
        [InlineKeyboardButton(text="{ التعطيل / التفعيل }", callback_data="cmd_toggle"), InlineKeyboardButton(text="{ القفل / الفتح }", callback_data="cmd_locks")],
        [InlineKeyboardButton(text="- قناة السورس .", url="https://t.me/BBABB9")]
    ])
    await message.reply("✧ ¦ CRYSTAL\n— — — — — — — — — —\n✧ ¦ اوامـر الـبـوت الـرئـيـسـيـة", reply_markup=keyboard)

@router.message(F.chat.type.in_({"group", "supergroup"}), lambda msg: msg.text and (msg.text.startswith("قفل ") or msg.text.startswith("فتح ")))
async def handle_locks_and_unlocks(message: Message):
    if not await is_admin(message): return
    parts = message.text.strip().split(" ", 1)
    action, target = parts[0], parts[1]
    settings = get_settings(message.chat.id)
    if target in settings:
        settings[target] = (action == "فتح")
        await message.reply(f"✔️ تم {'فتح' if action == 'فتح' else 'قفل'} **{target}** بنجاح.")

@router.message(F.chat.type.in_({"group", "supergroup"}))
async def monitor_group_messages(message: Message):
    if message.text:
        text_check = message.text.strip()
        if text_check in ["الاوامر", "تفعيل", "ايدي", "اسمي", "مطور", "المطور"] or text_check.startswith("قفل ") or text_check.startswith("فتح "):
            if text_check == "ايدي": await message.reply(f"🆔 ايديك » `{message.from_user.id}`\n🗂️ ايدي الكروب » `{message.chat.id}`")
            elif text_check == "اسمي": await message.reply(f"👤 اسمك الحركي » {message.from_user.first_name}")
            elif text_check in ["مطور", "المطور"]: await message.reply("👑 مطور السورس الغالي هو: @U_K44")
            return

    if await is_admin(message):
        if message.text and message.reply_to_message:
            text = message.text.strip()
            target_user = message.reply_to_message.from_user
            if text in ["طرد", "حظر"]:
                try: await message.chat.ban(user_id=target_user.id)
                except: pass
            elif text == "كتم":
                try: await message.chat.restrict(user_id=target_user.id, permissions=ChatPermissions(can_send_messages=False))
                except: pass
        return

    settings = get_settings(message.chat.id)
    if not settings["الكل"]:
        try: await message.delete()
        except: pass

    if message.text or message.caption:
        text = (message.text or message.caption).strip()
        if not settings["الروابط"] or not settings["المعرف"]:
            if "http" in text or "t.me/" in text or ".com" in text or "@" in text:
                try: await message.delete()
                except: pass
        if not settings["التاك"] and ("#" in text or "@" in text):
            try: await message.delete()
            except: pass
        if not settings["الكلايش"] and len(text) > 400:
            try: await message.delete()
            except: pass

    if not settings["التوجيه"] and message.forward_date:
        try: await message.delete()
        except: pass
    if not settings["الصور"] and message.photo:
        try: await message.delete()
        except: pass
    if not settings["الفيديو"] and message.video:
        try: await message.delete()
        except: pass
    if not settings["المتحركه"] and message.animation:
        try: await message.delete()
        except: pass
    if not settings["الملصقات"] and message.sticker:
        try: await message.delete()
        except: pass
    if not settings["الصوت"] and (message.voice or message.audio):
        try: await message.delete()
        except: pass
    if not settings["الملفات"] and message.document:
        try: await message.delete()
        except: pass
