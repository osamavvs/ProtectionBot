from aiogram import Router, F
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters import Command

router = Router()

# أمر الطرد (بالرد على الرسالة)
@router.message(F.text == "طرد")
async def ban_user(message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        try:
            await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=user_id)
            await message.reply("تم طرد العضو بنجاح 🚫")
            await message.delete()
        except:
            await message.reply("فشلت عملية الطرد! تأكد أنني مشرف ولدي صلاحيات.")

# الترحيب بالأعضاء الجدد
@router.chat_member()
async def welcome(event: ChatMemberUpdated):
    if event.new_chat_member.status == "member":
        user_name = event.new_chat_member.user.first_name
        await event.bot.send_message(
            event.chat.id, 
            f"أهلاً بك يا {user_name} في مجموعتنا! 🌹"
        )
