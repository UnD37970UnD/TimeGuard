import sqlite3

def setup_db():
    conn = sqlite3.connect('timeguard.db')
    cursor = conn.cursor()

    # Create a table for settings
    cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
                      id INTEGER PRIMARY KEY,
                      key TEXT UNIQUE,
                      value TEXT)''')

    # Create a table for users (with time_limit column)
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    enabled BOOLEAN,
                    time_limit INTEGER DEFAULT 0,
                    logout_time INTEGER DEFAULT 0)''')  # Default time limit is 0


    # Add time_limit column to existing users table if it doesn't exist
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'time_limit' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN time_limit INTEGER DEFAULT 0")

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

def get_user(username):
    conn = sqlite3.connect('timeguard.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result

def save_time(current_time, username):

    conn = sqlite3.connect('timeguard.db')
    cursor = conn.cursor()
    # Insert current time
    cursor.execute("UPDATE users SET logout_time=? WHERE username=?", (current_time, username))
    conn.commit()
    conn.close()
