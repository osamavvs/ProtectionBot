from aiogram import Router, F
from database import set_links_lock

router = Router()

@router.callback_query(F.data.in_(["lock_links", "unlock_links"]))
async def callback_query_handler(call):
    if call.data == "lock_links":
        await set_links_lock(call.message.chat.id, 1)
        await call.answer("تم قفل الروابط بنجاح ✅", show_alert=True)
    
    elif call.data == "unlock_links":
        await set_links_lock(call.message.chat.id, 0)
        await call.answer("تم فتح الروابط بنجاح ✅", show_alert=True)
