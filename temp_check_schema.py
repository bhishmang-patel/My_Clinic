import sqlite3

def print_table_info(db_path, table_name):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(f"PRAGMA table_info({table_name});")
    columns = c.fetchall()
    conn.close()
    print(f"Schema for table '{table_name}':")
    for col in columns:
        print(col)

if __name__ == "__main__":
    print_table_info("clinic.db", "consultation")
