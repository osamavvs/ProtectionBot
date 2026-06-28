from pyrogram import Client, filters
from database import get_lock_status

@Client.on_message(filters.group, group=1)
async def check_protection(client, message):
    # جلب حالة الأقفال للكروب الحالي من القاعدة
    links_lock, tags_lock, photos_lock = await get_lock_status(message.chat.id)
    
    # حماية الروابط
    if links_lock and (message.entities or message.caption_entities):
        # منطق فحص الروابط
        if any(e.type == "url" for e in (message.entities or [])):
            await message.delete()
            
    # حماية الصور
    if photos_lock and message.photo:
        await message.delete()
