import aiosqlite

# إنشاء قاعدة البيانات وتجهيز الجداول
async def init_db():
    async with aiosqlite.connect("bot_data.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                chat_id INTEGER PRIMARY KEY,
                is_links_locked INTEGER DEFAULT 0
            )
        """)
        await db.commit()

# دالة لتحديث حالة قفل الروابط
async def set_links_lock(chat_id, status):
    async with aiosqlite.connect("bot_data.db") as db:
        await db.execute("INSERT OR REPLACE INTO groups (chat_id, is_links_locked) VALUES (?, ?)", (chat_id, status))
        await db.commit()

# دالة للتحقق من حالة القفل
async def is_links_locked(chat_id):
    async with aiosqlite.connect("bot_data.db") as db:
        async with db.execute("SELECT is_links_locked FROM groups WHERE chat_id = ?", (chat_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0
