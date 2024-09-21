import subprocess
import sqlite3

def get_enabled_users():
    try:
        result = subprocess.run(['wmic', 'useraccount', 'where', 'disabled=false', 'get', 'name'], capture_output=True, text=True)
        users = result.stdout.splitlines()
        enabled_users = [user.strip() for user in users if user.strip() and user != 'Name']
        update_users_in_db(enabled_users[1:])
        return enabled_users[1:]
    except Exception as e:
        print(f"Error fetching enabled users: {e}")
        return []

def update_users_in_db(users):
    try:
        conn = sqlite3.connect('timeguard.db')
        cursor = conn.cursor()

        # Clear out existing enabled users before inserting new ones
        cursor.execute("DELETE FROM users")

        # Insert new users
        for user in users:
            cursor.execute("INSERT OR IGNORE INTO users (username, enabled) VALUES (?, ?)", (user, True))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating users in database: {e}")
        return False
