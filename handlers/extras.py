from aiogram import Router, F
from aiogram.types import Message, ChatMemberUpdated
import json, os

router = Router() # هذا السطر كان ناقصاً وهو سبب الخطأ

# كود الطرد (باقي كما هو)
@router.message(F.text == "طرد")
async def ban_user(message: Message):
    if message.reply_to_message:
        await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
        await message.reply("تم طرد العضو 🚫")
        await message.delete()

# كود الترحيب (باقي كما هو)
@router.chat_member()
async def welcome(event: ChatMemberUpdated):
    if event.new_chat_member.status == "member":
        await event.bot.send_message(event.chat.id, f"أهلاً بك {event.new_chat_member.user.first_name} في مجموعتنا! 🌹")

# كود رفع المطورين (جديد)
@router.message(F.text.startswith("رفع "))
async def promote_user(message: Message):
    # نتحقق من الآيدي الخاص بك
    if message.from_user.id != 8074717568: return
    if not message.reply_to_message: return await message.reply("يجب الرد على رسالة العضو!")
    
    target_id = message.reply_to_message.from_user.id
    rank = message.text.replace("رفع ", "")
    
    # حفظ الرتبة
    devs = {}
    if os.path.exists("devs.json"):
        with open("devs.json", "r") as f: 
            try: devs = json.load(f)
            except: devs = {}
    
    devs[str(target_id)] = rank
    with open("devs.json", "w") as f: json.dump(devs, f)
    
    await message.reply(f"تم رفع العضو لرتبة: {rank} ✅")
