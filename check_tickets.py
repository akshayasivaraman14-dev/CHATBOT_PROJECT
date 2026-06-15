import sqlite3

conn = sqlite3.connect("tickets.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM tickets")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()