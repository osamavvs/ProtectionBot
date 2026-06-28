from aiogram.filters import BaseFilter
from aiogram.types import Message
import os

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        # جلب آيدي الأدمن من المتغيرات البيئية
        admin_id = os.getenv("ADMIN_ID")
        if not admin_id:
            return False
        
        # التأكد من أن المستخدم هو الأدمن وأن المحادثة خاصة
        return message.from_user.id == int(admin_id) and message.chat.type == "private"
