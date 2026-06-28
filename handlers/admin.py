from pyrogram import Client, filters
from database import update_lock

@Client.on_message(filters.command("قفل_الروابط") & filters.group)
async def lock_links_cmd(client, message):
    await update_lock(message.chat.id, "links", 1)
    await message.reply("تم تفعيل قفل الروابط في القاعدة ✅")

@Client.on_message(filters.command("فتح_الروابط") & filters.group)
async def unlock_links_cmd(client, message):
    await update_lock(message.chat.id, "links", 0)
    await message.reply("تم إلغاء قفل الروابط في القاعدة ✅")
