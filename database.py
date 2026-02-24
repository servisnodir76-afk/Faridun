import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
diamond INTEGER DEFAULT 0,
premium INTEGER DEFAULT 0,
blocked INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS loads(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
text TEXT
)
""")

conn.commit()
