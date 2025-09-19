import sqlite3

conn = sqlite3.connect("clinic.db")
c = conn.cursor()

try:
    c.execute("ALTER TABLE consultation ADD COLUMN date TEXT;")
    print("Column 'date' added successfully.")
except sqlite3.OperationalError as e:
    print("Error:", e)

conn.commit()
conn.close()
