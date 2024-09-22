import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

from user_refresh import get_enabled_users, update_users_in_db
import user_refresh

class AdminPanel(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(expand=True, fill="both")

        # General tab
        self.general_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.general_tab, text="General")

        self.create_general_tab()

        # Get users and create tabs
        self.refresh_users()
        

    def create_general_tab(self):
        # Add widgets to the "General" tab
        general_label = tk.Label(self.general_tab, text="Admin General Settings")
        general_label.pack(pady=10)

        refresh_button = tk.Button(self.general_tab, text="Refresh Users", command=self.refresh_users)
        refresh_button.pack(pady=10)

    def load_user_tabs(self):
        users = self.get_users()
        tab_titles = [self.tabs.tab(i, "text") for i in range(self.tabs.index("end"))]
        for user in users:
            print(tab_titles)
            #check if tab already exists
            if(user['username'] not in tab_titles):
                self.create_user_tab(user)

    def refresh_users(self):
        user_refresh.get_enabled_users()
        self.load_user_tabs()
        
    def create_user_tab(self, user):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text=user['username'])

        # Add user-specific form elements here, e.g., screen time limit
        tk.Label(tab, text=f"Settings for {user['username']}").pack(pady=10)

        tk.Label(tab, text="Time Limit (minutes):").pack(pady=5)
        time_limit_entry = tk.Entry(tab)
        time_limit_entry.pack(pady=5)

        # Pre-fill user-specific settings (if any), like time limits
        if user['time_limit']:
            time_limit_entry.insert(0, user['time_limit'])

        # Save button to store settings in the database
        save_button = tk.Button(tab, text="Save", command=lambda: self.save_user_settings(user['username'], time_limit_entry.get()))
        save_button.pack(pady=10)

    def get_users(self):
        # Fetch enabled users from the database
        conn = sqlite3.connect('timeguard.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username, time_limit FROM users")
        users = cursor.fetchall()
        conn.close()

        return [{'username': row[0], 'time_limit': row[1]} for row in users]

    def save_user_settings(self, username, time_limit):
        # Save the user's settings (like time limit) to the database
        conn = sqlite3.connect('timeguard.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET time_limit=? WHERE username=?", (time_limit, username))
        conn.commit()
        conn.close()

