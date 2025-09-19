# database/db_queries.py
import sqlite3

def register_doctor(name, clinic, phone, password, pin):
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()
    c.execute('INSERT INTO doctor (name, clinic_name, phone, password, pin) VALUES (?, ?, ?, ?, ?)',
              (name, clinic, phone, password, pin))
    conn.commit()
    conn.close()

def check_login(phone, password):
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()
    c.execute('SELECT * FROM doctor WHERE phone=? AND password=?', (phone, password))
    doctor = c.fetchone()
    conn.close()
    return doctor

def load_dashboard(doctor):
    from ui.dashboard_ui import Dashboard
    win = Dashboard(doctor)
    win.show()
    return win

def delete_consultation_log(log_id):
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()
    c.execute('DELETE FROM consultation WHERE id=?', (log_id,))
    conn.commit()
    conn.close()
