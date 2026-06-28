from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# دالة عرض القائمة الرئيسية للأوامر بالأزرار الشفافة
@router.message(F.chat.type.in_({"group", "supergroup"}), F.text == "الاوامر")
async def send_group_commands(message: Message):
    if not await is_admin(message): return
    
    # نص الرسالة الرئيسية كما في الصورة
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

    # تصميم الأزرار الشفافة (Inline Keyboard) بنفس ترتيب الصورة 25718.jpg
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
            InlineKeyboardButton(text="- قناة السورس .", url="https://t.me/YourChannel") # ضع رابط قناتك هنا
        ]
    ])
    
    await message.reply(text=main_text, reply_markup=keyboard)
@router.message(F.chat.type.in_({"group", "supergroup"}))
async def handle_crystal_source(message: Message):
    if not message.text: return
    text = message.text.strip()
    
    # [أولاً] أوامر المشرفين بالرد السريع
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

    # [ثانياً] الحماية التلقائية للأعضاء العاديين
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

    # [ثالثاً] أوامر معلومات الأعضاء
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
            await message.reply(f"🔗 رابط المجموعة الخاص بسورس كرستال:\n{link}")
        except:
            await message.reply("❌ البوت يحتاج إلى صلاحية إدارة الروابط لاستخراج الرابط.")

    # [رابعاً] قسم التسلية والردود السريعة
    elif text == "هلو":
        await message.reply(f"هلا عيني {message.from_user.first_name}، نورت سورس كرستال 💎")
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
        await message.reply(f"🐦 تـويـت كرستال: {random.choice(tweets)}")
    elif text == "كول":
        sayings = ["من حفر حفرة لأخيه وقع فيها.", "الصمت حكمه وقليل فاعله.", "الوقت كالسيف إن لم تقطعه قطعك."]
        await message.reply(f"💬 كول المأثور: {random.choice(sayings)}")
