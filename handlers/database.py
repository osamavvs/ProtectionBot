import aiosqlite

# دالة لإنشاء القاعدة والجداول
async def init_db():
    async with aiosqlite.connect("bot_data.db") as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS groups_settings (
                chat_id INTEGER PRIMARY KEY,
                links INTEGER DEFAULT 0,
                tags INTEGER DEFAULT 0,
                photos INTEGER DEFAULT 0
            )
        ''')
        await db.commit()

# دالة لجلب حالة القفل
async def get_lock_status(chat_id):
    async with aiosqlite.connect("bot_data.db") as db:
        cursor = await db.execute('SELECT links, tags, photos FROM groups_settings WHERE chat_id = ?', (chat_id,))
        row = await cursor.fetchone()
        return row if row else (0, 0, 0) # افتراضياً الكل مفتوح (0)

# دالة لتغيير حالة القفل
async def update_lock(chat_id, column, value):
    async with aiosqlite.connect("bot_data.db") as db:
        await db.execute(f'INSERT OR REPLACE INTO groups_settings (chat_id, {column}) VALUES (?, ?)', (chat_id, value))
        await db.commit()

