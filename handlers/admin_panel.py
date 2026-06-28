from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import json, os

router = Router()
ADMIN_ID = 8074717568

# دالة لجلب القائمة الرئيسية (لضمان عمل زر الرجوع)
def main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛠 اوامر الادارة", callback_data="admin_menu")],
        [InlineKeyboardButton(text="🔒 الفتح والقفل", callback_data="lock_menu")],
        [InlineKeyboardButton(text="👤 اوامر الاعضاء", callback_data="member_menu")],
        [InlineKeyboardButton(text="🛡 المضاد", callback_data="anti_menu")],
        [InlineKeyboardButton(text="Source", url="https://t.me/BBABB9")] # زر الحقوق
    ])

@router.message(F.text == "الاوامر")
async def show_main_menu(message: Message):
    if message.from_user.id != ADMIN_ID: return
    await message.reply("📋 **قائمة التحكم الرئيسية - سورس العمدة:**", reply_markup=main_keyboard())
    await message.delete()

# --- معالجة زر الرجوع ---
@router.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):
    await callback.message.edit_text("📋 **قائمة التحكم الرئيسية - سورس العمدة:**", reply_markup=main_keyboard())

# --- قسم الرفع (المطورين) ---
@router.callback_query(F.data == "admin_menu")
async def admin_menu(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="رفع ادمن", callback_data="set_admin"), 
         InlineKeyboardButton(text="رفع منشئ", callback_data="set_owner")],
        [InlineKeyboardButton(text="رفع مطور اساسي", callback_data="set_dev1")],
        [InlineKeyboardButton(text="رجوع", callback_data="back_main")]
    ])
    await callback.message.edit_text("🛠 **اختر نوع الرفع:**\n(قم بالرد على رسالة الشخص لرفعه)", reply_markup=kb)

# --- كود رفع المطورين (منطقي) ---
@router.callback_query(F.data.in_(["set_admin", "set_owner", "set_dev1"]))
async def set_ranks(callback: CallbackQuery):
    # ملاحظة: هذا يتطلب أن يكون الأمر بالرد على رسالة العضو
    await callback.answer("يرجى الرد على رسالة العضو بكلمة 'رفع' لتفعيل الرتبة", show_alert=True)
