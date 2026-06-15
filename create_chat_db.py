import sqlite3

conn = sqlite3.connect("tickets.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history(

id INTEGER PRIMARY KEY AUTOINCREMENT,

question TEXT,

answer TEXT,

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()
conn.close()

print("Chat table created")