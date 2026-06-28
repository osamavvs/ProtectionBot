from pyrogram import Client, filters

# قواميس للحالات (في السورس الحقيقي نربطها بقاعدة بيانات)
locks = {
    "links": True,
    "tags": True,
    "photos": True,
    "spam": True
}

# 1. حماية الروابط
@Client.on_message(filters.regex(r"https?://\S+") & filters.group, group=1)
async def protect_links(client, message):
    if locks["links"]:
        await message.delete()

# 2. حماية التاك (المنشن)
@Client.on_message(filters.mention & filters.group, group=2)
async def protect_tags(client, message):
    if locks["tags"]:
        await message.delete()

# 3. حماية الصور
@Client.on_message(filters.photo & filters.group, group=3)
async def protect_photos(client, message):
    if locks["photos"]:
        await message.delete()

# 4. حماية الرسائل المكررة (Spam - منطق بسيط)
@Client.on_message(filters.text & filters.group, group=4)
async def protect_spam(client, message):
    # هنا يضاف منطق فحص الرسائل المكررة
    pass
