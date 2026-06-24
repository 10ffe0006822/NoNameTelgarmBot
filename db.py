import sqlite3

conn = sqlite3.connect("data/db.sqlite3")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS chat_ids (id INTEGER PRIMARY KEY, chat_id TEXT, chat_name TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS admin_ids (id INTEGER PRIMARY KEY, admin_id TEXT)")
conn.commit()
async def add_chat_id(chat_id, chat_name):
    global cursor
    cursor.execute("INSERT INTO chat_ids (chat_id, chat_name) VALUES (?, ?)", (chat_id, chat_name))
    conn.commit()

async def remove_chat_id(chat_id):
    global cursor
    cursor.execute("DELETE FROM chat_ids WHERE chat_id = ?", (chat_id,))
    conn.commit()

async def get_chat_id():
    global cursor
    cursor.execute("SELECT * FROM chat_ids")
    chat_ids = cursor.fetchall()
    clear_ids = []
    for chat_id in chat_ids:
        clear_ids.append(chat_id[1])
    return clear_ids

async def get_chat_name():
    global cursor
    cursor.execute("SELECT * FROM chat_ids")
    chat_names = cursor.fetchall()
    clear_ids = []
    for chat_name in chat_names:
        clear_ids.append(chat_name[2])
    return clear_ids


async def add_admin_id(user_id):
    global cursor
    cursor.execute("INSERT INTO admin_ids (admin_id) VALUES (?)", (user_id,))
    conn.commit()

async def remove_admin_id(user_id):
    global cursor
    cursor.execute("DELETE FROM admin_ids WHERE admin_id = ?", (user_id,))
    conn.commit()

async def get_admin_id():
    global cursor
    cursor.execute("SELECT * FROM admin_ids")
    admin_ids = cursor.fetchall()
    clear_ids = []
    for admin_id in admin_ids:
        clear_ids.append(admin_id[1])
    return clear_ids