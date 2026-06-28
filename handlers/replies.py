from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()

# حالات نظام الردود التلقائية (FSM)
class ReplyStates(StatesGroup):
    waiting_for_word = State()
    waiting_for_reply = State()
    waiting_for_del_word = State()

async def is_admin(message: Message) -> bool:
    if message.chat.type == "private":
        return False
    member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    return member.status in ["creator", "administrator"]

# --- دالات ملف الردود النصي l444q.txt ---
def add_rd(chat_id, word, reply_text):
    with open("l444q.txt", "a+", encoding="utf-8") as f:
        f.write(f"{chat_id}#{word}𚔁444𝚇{reply_text}\n")

def get_rd(chat_id, word):
    try:
        with open("l444q.txt", "r", encoding="utf-8") as f:
            for line in f:
                if line.strip() and f"{chat_id}#{word}𚔁444𝚇" in line:
                    return line.split("𚔁444𝚇")[1].strip()
    except FileNotFoundError:
        pass
    return None

def del_rd(chat_id, word):
    try:
        with open("l444q.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open("l444q.txt", "w", encoding="utf-8") as f:
            deleted = False
            for line in lines:
                if f"{chat_id}#{word}𚔁444𝚇" in line:
                    deleted = True
                    continue
                f.write(line)
            return deleted
    except FileNotFoundError:
        return False

def del_all_rd(chat_id):
    try:
        with open("l444q.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open("l444q.txt", "w", encoding="utf-8") as f:
            has_replies = False
            for line in lines:
                if str(chat_id) in line.split("#")[0]:
                    has_replies = True
                    continue
                f.write(line)
            return has_replies
    except FileNotFoundError:
        return False

def get_all_rd_list(chat_id):
    text = "• الردود بهذه المجموعة : \n"
    found = False
    try:
        with open("l444q.txt", "r", encoding="utf-8") as f:
            for line in f:
                if line.strip() and str(chat_id) in line.split("#")[0]:
                    word = line.split("#")[1].split("𚔁444𝚇")[0]
                    text += f"— {word}\n"
                    found = True
    except FileNotFoundError:
        pass
    return text if found else None

# --- التحكم في إضافة ومسح الردود ---
@router.message(F.chat.type.in_({"group", "supergroup"}), F.text == "اضف رد")
async def start_add_reply(message: Message, state: FSMContext):
    if not await is_admin(message): return await message.reply("• هذا الأمر لا يخصك")
    await state.set_state(ReplyStates.waiting_for_word)
    await message.reply("ارسل كلمة الرد الآن")

@router.message(ReplyStates.waiting_for_word, F.text)
async def process_reply_word(message: Message, state: FSMContext):
    await state.update_data(word=message.text.strip())
    await state.set_state(ReplyStates.waiting_for_reply)
    await message.reply("ارسل جواب الرد الآن")

@router.message(ReplyStates.waiting_for_reply, F.text)
async def process_reply_text(message: Message, state: FSMContext):
    data = await state.get_data()
    word = data['word']
    reply_text = message.text.strip()
    add_rd(message.chat.id, word, reply_text)
    await state.clear()
    await message.reply("تم اضافة الرد بنجاح")

@router.message(F.chat.type.in_({"group", "supergroup"}), F.text == "مسح رد")
async def start_del_reply(message: Message, state: FSMContext):
    if not await is_admin(message): return await message.reply("• هذا الأمر لا يخصك")
    await state.set_state(ReplyStates.waiting_for_del_word)
    await message.reply("ارسل الرد الذي تريد مسحه الآن")

@router.message(ReplyStates.waiting_for_del_word, F.text)
async def process_del_reply(message: Message, state: FSMContext):
    word = message.text.strip()
    if del_rd(message.chat.id, word):
        await message.reply("• تم مسح الرد بنجاح")
    else:
        await message.reply("الرد غير موجود")
    await state.clear()

@router.message(F.chat.type.in_({"group", "supergroup"}), F.text == "مسح الردود")
async def delete_all_group_replies(message: Message):
    if not await is_admin(message): return await message.reply("• هذا الأمر لا يخصك")
    if del_all_rd(message.chat.id):
        await message.reply("• تم مسح الردود هنا")
    else:
        await message.reply("• لاتوجد ردود هنا")

@router.message(F.chat.type.in_({"group", "supergroup"}), F.text == "الردود")
async def list_group_replies(message: Message):
    if not await is_admin(message): return await message.reply("• هذا الأمر لا يخصك")
    res = get_all_rd_list(message.chat.id)
    await message.reply(res if res else "• لا توجد ردود هنا")
