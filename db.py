import sqlite3
import asyncio

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS chat_ids (id INTEGER PRIMARY KEY, chat_id TEXT, chat_name TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS admin_ids (id INTEGER PRIMARY KEY, admin_id TEXT)")
cursor.close()
conn.commit()
conn.close()

async def add_chat_id(chat_id, chat_name):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_ids (chat_id, chat_name) VALUES (?, ?)", (chat_id, chat_name))
    conn.commit()
    cursor.close()
    conn.close()

async def remove_chat_id(chat_id):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_ids WHERE chat_id = ?", (chat_id,))
    conn.commit()
    cursor.close()
    conn.close()

async def get_chat_id():
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chat_ids")
    ids = cursor.fetchall()
    clear_ids = []
    conn.commit()
    cursor.close()
    conn.close()
    for id in ids:
        clear_ids.append(id[1])
    return clear_ids

async def get_chat_name():
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chat_ids")
    ids = cursor.fetchall()
    clear_ids = []
    conn.commit()
    cursor.close()
    conn.close()
    for id in ids:
        clear_ids.append(id[2])
    return clear_ids


async def add_admin_id(user_id):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO admin_ids (admin_id) VALUES (?)", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

async def remove_admin_id(user_id):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM admin_ids WHERE admin_id = ?", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

async def get_admin_id():
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin_ids")
    ids = cursor.fetchall()
    clear_ids = []
    conn.commit()
    cursor.close()
    conn.close()
    for id in ids:
        clear_ids.append(id[1])
    return clear_ids