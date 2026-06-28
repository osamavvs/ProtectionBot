from pyrogram import Client, filters

@Client.on_message(filters.group & filters.regex(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"))
async def delete_links(client, message):
    # مسح الرابط تلقائياً
    await message.delete()
    await message.reply(f"🚫 تم حذف الرابط يا {message.from_user.mention}، يمنع نشر الروابط!")
