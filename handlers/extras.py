from aiogram import Router, F
from aiogram.types import Message, ChatMemberUpdated

router = Router()

@router.message(F.text == "طرد")
async def ban_user(message: Message):
    if message.reply_to_message:
        await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
        await message.reply("تم طرد العضو 🚫")
        await message.delete()

@router.chat_member()
async def welcome(event: ChatMemberUpdated):
    if event.new_chat_member.status == "member":
        await event.bot.send_message(event.chat.id, f"أهلاً بك {event.new_chat_member.user.first_name} في مجموعتنا! 🌹")
