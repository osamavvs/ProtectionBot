@router.message(F.text.startswith("رفع "))
async def promote_user(message: Message):
    if message.from_user.id != 8074717568: return # حماية للمنشئ فقط
    if not message.reply_to_message: return await message.reply("يجب الرد على رسالة العضو!")
    
    target_id = message.reply_to_message.from_user.id
    rank = message.text.replace("رفع ", "")
    
    # حفظ الرتبة في ملف
    devs = {}
    if os.path.exists("devs.json"):
        with open("devs.json", "r") as f: devs = json.load(f)
    
    devs[str(target_id)] = rank
    with open("devs.json", "w") as f: json.dump(devs, f)
    
    await message.reply(f"تم رفع العضو لرتبة: {rank} ✅")
