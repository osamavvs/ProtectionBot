from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import json, os

router = Router()
ADMIN_ID = 8074717568
DB_FILE = "id_settings.json"

# مخزن أشكال الأيدي (يمكنك إضافة 10 أشكال هنا)
CARDS = {
    "1": "✨ تصميم الأيدي رقم 1\nالاسم: {name}\nالآيدي: {id}",
    "2": "👑 تصميم الأيدي رقم 2\n[-- {name} --]\n[-- {id} --]",
    "3": "💎 تصميم الأيدي رقم 3\nID: {id} | User: {name}",
    # أضف باقي الـ 10 تصاميم بنفس الطريقة...
}

def get_current_card():
    if not os.path.exists(DB_FILE): return "1"
    with open(DB_FILE, "r") as f: return json.load(f).get("selected", "1")

# عرض الأيدي للجميع
@router.message(F.text.in_({"ايدي", "id"}))
async def show_id(message: Message):
    card_id = get_current_card()
    template = CARDS.get(card_id, CARDS["1"])
    text = template.format(name=message.from_user.first_name, id=message.from_user.id)
    await message.reply(text)

# تغيير الأيدي (للمنشئ فقط)
@router.message(F.text == "تغيير الايدي")
async def edit_id_cmd(message: Message):
    if message.from_user.id != ADMIN_ID: return
    current = get_current_card()
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️", callback_data="prev_id"), InlineKeyboardButton(text="➡️", callback_data="next_id")],
        [InlineKeyboardButton(text="✅ حفظ الاختيار", callback_data="save_id")]
    ])
    await message.reply(f"اختر تصميم الأيدي (الحالي: {current}):\n{CARDS[current].format(name='تجربة', id='12345')}", reply_markup=kb)

@router.callback_query(F.data.in_({"prev_id", "next_id", "save_id"}))
async def manage_id_selection(callback: CallbackQuery):
    current = int(get_current_card())
    if callback.data == "next_id": current = (current % len(CARDS)) + 1
    elif callback.data == "prev_id": current = (current - 2) % len(CARDS) + 1
    
    if callback.data == "save_id":
        with open(DB_FILE, "w") as f: json.dump({"selected": str(current)}, f)
        await callback.answer("تم حفظ التصميم بنجاح!")
    else:
        new_text = f"تصميم الأيدي ({current}):\n{CARDS[str(current)].format(name='تجربة', id='12345')}"
        await callback.message.edit_text(new_text, reply_markup=callback.message.reply_markup)
