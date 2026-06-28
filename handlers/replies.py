from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()

class ReplyStates(StatesGroup):
    waiting_for_word = State()
    waiting_for_reply = State()

async def is_admin(message: Message) -> bool:
    if message.chat.type == "private": return False
    member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    return member.status in ["creator", "administrator"]

# --- معالجة إضافة الردود ---
@router.message(F.text == "اضف رد")
async def start_add_reply(message: Message, state: FSMContext):
    if not await is_admin(message): return
    await state.set_state(ReplyStates.waiting_for_word)
    await message.reply("ارسل كلمة الرد الآن")

@router.message(ReplyStates.waiting_for_word)
async def process_reply_word(message: Message, state: FSMContext):
    await state.update_data(word=message.text.strip())
    await state.set_state(ReplyStates.waiting_for_reply)
    await message.reply("ارسل جواب الرد الآن")

@router.message(ReplyStates.waiting_for_reply)
async def process_reply_text(message: Message, state: FSMContext):
    data = await state.get_data()
    word = data['word']
    with open("l444q.txt", "a+", encoding="utf-8") as f:
        f.write(f"{message.chat.id}#{word}𚔁444𝚇{message.text.strip()}\n")
    await state.clear()
    await message.reply("تم اضافة الرد بنجاح")

# --- الدالة الأساسية لإرسال الردود (يجب أن تكون آخر دالة في الملف) ---
@router.message(F.chat.type.in_({"group", "supergroup"}), F.text)
async def check_reply(message: Message):
    # لا ترد إذا كان الأمر يخص الإدارة
    if message.text in ["اضف رد", "مسح رد", "مسح الردود", "الردود"]:
        return
        
    text_check = message.text.strip()
    try:
        with open("l444q.txt", "r", encoding="utf-8") as f:
            for line in f:
                if f"{message.chat.id}#{text_check}𚔁444𝚇" in line:
                    reply = line.split("𚔁444𝚇")[1].strip()
                    await message.reply(reply)
                    return # الخروج لضمان عدم تداخل الردود
    except: pass
