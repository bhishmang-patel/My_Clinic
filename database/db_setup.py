import sqlite3

def create_tables():
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()

    # Doctor table
    c.execute('''
    CREATE TABLE IF NOT EXISTS doctor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        clinic_name TEXT,
        phone TEXT,
        password TEXT,
        pin TEXT
    )
    ''')

    # Patient table
    c.execute('''
    CREATE TABLE IF NOT EXISTS patient (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        address TEXT,
        phone TEXT
    )
    ''')

    # Consultation table (FINAL structure)
    c.execute('''
    CREATE TABLE IF NOT EXISTS consultation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        complaints TEXT,
        treatments TEXT,
        duration TEXT,
        report TEXT,
        charge REAL,
        doctor_id INTEGER,
        FOREIGN KEY (patient_id) REFERENCES patient(id),
        FOREIGN KEY (doctor_id) REFERENCES doctor(id)
    )
    ''')

    # Clean up: Remove obsolete columns check
    # No 'symptoms', 'disease', 'tablets', 'bill_amount' anymore!

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
