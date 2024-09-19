import sqlite3

def create_db():
    conn = sqlite3.connect('parental_control.db')
    c = conn.cursor()
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS time_limits (
                    user TEXT, time_limit INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS user_logs (
                    user TEXT, event TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def save_time_limit(user, time_limit):
    conn = sqlite3.connect('parental_control.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO time_limits (user, time_limit) VALUES (?, ?)", (user, time_limit))
    conn.commit()
    conn.close()

def log_time(user, remaining_time):
    conn = sqlite3.connect('parental_control.db')
    c = conn.cursor()
    c.execute("INSERT INTO user_logs (user, event) VALUES (?, ?)", (user, f"Remaining time: {remaining_time}s"))
    conn.commit()
    conn.close()

def log_event(user, event):
    conn = sqlite3.connect('parental_control.db')
    c = conn.cursor()
    c.execute("INSERT INTO user_logs (user, event) VALUES (?, ?)", (user, event))
    conn.commit()
    conn.close()

create_db()  # Initialize the database at the start
