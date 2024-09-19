import sqlite3
from datetime import datetime

def create_db():
    conn = sqlite3.connect('parental_control.db')
    c = conn.cursor()
    # Create tables
    print("[INFO] Creating tables if not already present...")
    c.execute('''CREATE TABLE IF NOT EXISTS time_limits (
                    user TEXT, time_limit INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS user_logs (
                    user TEXT, event TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS user_login (
                    user TEXT, login_time DATETIME)''')
    conn.commit()
    conn.close()
    print("[INFO] Database setup complete.")

def save_time_limit(user, time_limit):
    print(f"[INFO] Saving time limit for user: {user}, Time: {time_limit}")
    conn = sqlite3.connect('parental_control.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO time_limits (user, time_limit) VALUES (?, ?)", (user, time_limit))
    conn.commit()
    conn.close()

def save_login_time(user):
    login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[INFO] Saving login time for {user}: {login_time}")
    conn = sqlite3.connect('parental_control.db')
    c = conn.cursor()
    c.execute("INSERT INTO user_login (user, login_time) VALUES (?, ?)", (user, login_time))
    conn.commit()
    conn.close()

def get_login_time(user):
    conn = sqlite3.connect('parental_control.db')
    c = conn.cursor()
    c.execute("SELECT login_time FROM user_login WHERE user = ?", (user,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def get_time_limit(user):
    conn = sqlite3.connect('parental_control.db')
    c = conn.cursor()
    c.execute("SELECT time_limit FROM time_limits WHERE user = ?", (user,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def get_all_users():
    conn = sqlite3.connect('parental_control.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT user FROM user_login")
    users = c.fetchall()
    conn.close()
    return [user[0] for user in users]

create_db()
