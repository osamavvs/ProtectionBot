from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# دالة التعامل مع ضغطة زر { 1 } أوامر الحماية لـ سورس كرستال
@router.callback_query(F.data == "cmd_1")
async def show_protection_commands(callback: CallbackQuery):
    protection_text = """✧ ¦ CRYSTAL
— — — — — — — — — —
✧ ¦ اوامر الحمايه كالاتي ...
— — — — — — — — — —
✧ ¦ قفل ، فتح ← الامر
✧ ¦ تستطيع قفل حمايه كما يلي ...
✧ ¦ ← { بالتقييد ، بالطرد ، بالكتم }
— — — — — — — — — —
✧ ¦ الكل ~ الدخول
✧ ¦ الروابط ~ المعرف
✧ ¦ التاك ~ الشارحه
✧ ¦ التعديل ~ تعديل الميديا
✧ ¦ المتحركه ~ الملفات
✧ ¦ الصور ~ الفيديو
✧ ¦ الستوري = توجية الستوري
— — — — — — — — — —
✧ ¦ الماركدوان ~ البوتات
✧ ¦ التكرار ~ الكلايش
✧ ¦ السيلفي ~ الملصقات
✧ ¦ الانلاين ~ الدردشه
— — — — — — — — — —
✧ ¦ التوجيه ~ الاغاني
✧ ¦ الصوت ~ الجهات
✧ ¦ الاشعارات ~ التثبيت
✧ ¦ الوسائط ~ التفليش
✧ ¦ وسائط المميزين
✧ ¦ الفشار ~ ارسال القناة
✧ ¦ القنوات
✧ ¦ الإنكليزيه ~ الفارسيه
✧ ¦ الكفر ~ الاباحي
— — — — — — — — — —"""

    # زر رجوع للقائمة الرئيسية
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 رجوع", callback_data="back_to_main")]
    ])

    # تعديل الرسالة الحالية بسلاسة لتظهر أوامر الحماية
    await callback.message.edit_text(text=protection_text, reply_markup=keyboard)
    await callback.answer()


# دالة زر الرجوع للقائمة الرئيسية للأوامر
@router.callback_query(F.data == "back_to_main")
async def back_to_main_menu(callback: CallbackQuery):
    main_text = """✧ ¦ اوامـر الـبـوت الـرئـيـسـيـة
— — — — — — — — — —
✧ ¦ م1 ← اوامر الحمايه
✧ ¦ م2 ← اوامر الادمنيه
✧ ¦ م3 ← اوامر المدراء
✧ ¦ م4 ← اوامر المنشئين
✧ ¦ م5 ← اوامر المالكين
✧ ¦ م6 ← اوامر التحشيش
✧ ¦ م7 ← اوامر المطور
✧ ¦ م8 ← اوامر التسليه
✧ ¦ م9 ← اوامر البنك"""

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="{ 2 }", callback_data="cmd_2"),
            InlineKeyboardButton(text="{ 1 }", callback_data="cmd_1")
        ],
        [
            InlineKeyboardButton(text="{ 4 }", callback_data="cmd_4"),
            InlineKeyboardButton(text="{ 3 }", callback_data="cmd_3")
        ],
        [
            InlineKeyboardButton(text="{ 6 }", callback_data="cmd_6"),
            InlineKeyboardButton(text="{ 5 }", callback_data="cmd_5")
        ],
        [
            InlineKeyboardButton(text="{ الالعاب }", callback_data="cmd_games"),
            InlineKeyboardButton(text="{ م7 }", callback_data="cmd_7")
        ],
        [
            InlineKeyboardButton(text="{ اوامر البنك }", callback_data="cmd_bank"),
            InlineKeyboardButton(text="{ اوامر التسليه }", callback_data="cmd_8")
        ],
        [
            InlineKeyboardButton(text="{ التعطيل / التفعيل }", callback_data="cmd_toggle"),
            InlineKeyboardButton(text="{ القفل / الفتح }", callback_data="cmd_locks")
        ],
        [
            InlineKeyboardButton(text="- قناة السورس .", url="https://t.me/BBABB9")
        ]
    ])

    await callback.message.edit_text(text=main_text, reply_markup=keyboard)
    await callback.answer()
