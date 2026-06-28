from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus

# دالة الايدي (ايدي)
@Client.on_message(filters.regex("^ايدي$"))
async def myid(client, message):
   member = await message.chat.get_member(message.from_user.id)
   status = "المالك" if member.status == ChatMemberStatus.OWNER else \
            "المشرف" if member.status == ChatMemberStatus.ADMINISTRATOR else "العضو"
   
   a = await client.get_chat(message.from_user.id)
   name = message.from_user.mention
   username = message.from_user.username or "لايوجد"
   bio = a.bio or "لا يوجد"
   
   caption = f"اسمك : {name}\nمعرفك : @{username}\nايديك : `{message.from_user.id}`\nرتبتك : {status}\n- {bio}"
   
   if a.photo:
      async for photo in client.get_chat_photos(message.from_user.id, limit=1):
         await message.reply_photo(photo.file_id, caption=caption)
   else:
      await message.reply(caption)
