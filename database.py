import sqlite3

def setup_db():
    conn = sqlite3.connect('timeguard.db')
    cursor = conn.cursor()
    # Create a table for settings
    cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
                      id INTEGER PRIMARY KEY,
                      key TEXT UNIQUE,
                      value TEXT)''')
    # Create a table for users
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY,
                      username TEXT UNIQUE,
                      enabled BOOLEAN)''')
    conn.commit()
    conn.close()

def is_first_run():
    conn = sqlite3.connect('timeguard.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM settings WHERE key='admin_password'")
    result = cursor.fetchone()
    conn.close()
    return result[0] == 0

def get_admin_password():
    conn = sqlite3.connect('timeguard.db')
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key='admin_password'")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else ""
