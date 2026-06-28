from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import json, os

router = Router()
ADMIN_ID = 8074717568

# القائمة الرئيسية للأوامر
@router.message(F.text == "الاوامر")
async def show_main_menu(message: Message):
    if message.from_user.id != ADMIN_ID: return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛠 اوامر الادارة", callback_data="admin_menu")],
        [InlineKeyboardButton(text="🔒 الفتح والقفل", callback_data="lock_menu")],
        [InlineKeyboardButton(text="👤 اوامر الاعضاء", callback_data="member_menu")],
        [InlineKeyboardButton(text="🎮 الالعاب", callback_data="game_menu")],
        [InlineKeyboardButton(text="🛡 المضاد", callback_data="anti_menu")],
        [InlineKeyboardButton(text="Source @BBABB9", url="https://t.me/BBABB9")] # زر الحقوق
    ])
    await message.reply("📋 **قائمة التحكم الرئيسية - سورس العمدة:**", reply_markup=keyboard)

# القائمة الفرعية (مثال: أوامر الرفع)
@router.callback_query(F.data == "admin_menu")
async def admin_menu(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="رفع ادمن", callback_data="set_admin"), 
         InlineKeyboardButton(text="رفع منشئ", callback_data="set_owner")],
        [InlineKeyboardButton(text="رفع مطور ثانوي", callback_data="set_dev2"), 
         InlineKeyboardButton(text="رفع مطور اساسي", callback_data="set_dev1")],
        [InlineKeyboardButton(text="رجوع", callback_data="back_main")]
    ])
    await callback.message.edit_text("🛠 **اوامر الرفع والادارة:**", reply_markup=kb)

# زر الرجوع
@router.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):
    await show_main_menu(callback.message)
