from aiogram import Router, F
from aiogram.types import Message

router = Router()

# دالة مساعدة للتأكد إذا كان الشخص الذي أرسل الأمر هو أدمن (مشرف) بالقروب
async def is_admin(message: Message) -> bool:
    member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    return member.status in ["creator", "administrator"]

# أمر (طرد) بالرد على الشخص بدون /
@router.message(F.text == "طرد")
async def ban_user(message: Message):
    if not await is_admin(message):
        return
    
    if not message.reply_to_message:
        await message.reply("⚠️ عيني، لازم تسوي رد (reply) على رسالة الشخص اللي تريد تطرده.")
        return
        
    user_id = message.reply_to_message.from_user.id
    try:
        await message.chat.ban(user_id=user_id)
        await message.reply(f"👤 تم طرد العضو {message.reply_to_message.from_user.full_name} بنجاح!")
    except Exception as e:
        await message.reply("❌ البوت ما عنده صلاحية طرد هذا الشخص أو رتبته أعلى من البوت.")

# أمر (كتم) بالرد على الشخص بدون /
@router.message(F.text == "كتم")
async def mute_user(message: Message):
    if not await is_admin(message):
        return
        
    if not message.reply_to_message:
        await message.reply("⚠️ عيني، لازم تسوي رد (reply) على رسالة الشخص اللي تريد تكتمه.")
        return
        
    user_id = message.reply_to_message.from_user.id
    try:
        from aiogram.types import ChatPermissions
        permissions = ChatPermissions(can_send_messages=False)
        await message.chat.restrict(user_id=user_id, permissions=permissions)
        await message.reply(f"🔇 تم كتم العضو {message.reply_to_message.from_user.full_name}!")
    except Exception as e:
        await message.reply("❌ ما قدرت أكتم العضو، تأكد من صلاحيات البوت.")

# أمر (الغاء الكتم) بالرد على الشخص بدون /
@router.message(F.text == "الغاء الكتم")
async def unmute_user(message: Message):
    if not await is_admin(message):
        return
        
    if not message.reply_to_message:
        await message.reply("⚠️ عيني، لازم تسوي رد (reply) على الشخص لإلغاء كتمه.")
        return
        
    user_id = message.reply_to_message.from_user.id
    try:
        from aiogram.types import ChatPermissions
        permissions = ChatPermissions(
            can_send_messages=True, 
            can_send_audios=True, 
            can_send_documents=True, 
            can_send_photos=True, 
            can_send_videos=True
        )
        await message.chat.restrict(user_id=user_id, permissions=permissions)
        await message.reply(f"🔊 تم إلغاء الكتم عن العضو {message.reply_to_message.from_user.full_name}، تكدر تسولف هسة.")
    except Exception as e:
        await message.reply("❌ فشل إلغاء الكتم.")
