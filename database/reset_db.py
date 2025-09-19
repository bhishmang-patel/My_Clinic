import sqlite3

conn = sqlite3.connect('clinic.db')
c = conn.cursor()

# Wipe all consultations & patients
c.execute("DELETE FROM consultation;")
c.execute("DELETE FROM patient;")

conn.commit()
conn.close()

print("All patient and consultation data cleared.")
