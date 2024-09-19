import tkinter as tk
from tkinter import ttk
import sqlite3

class AdminPanel(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.general_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.general_tab, text="General")

        # Load user tabs
        self.load_user_tabs()

    def load_user_tabs(self):
        self.notebook.forget(self.general_tab)  # Remove existing tabs except General
        self.general_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.general_tab, text="General")

        conn = sqlite3.connect('timeguard.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE enabled = 1")
        users = cursor.fetchall()
        conn.close()

        for user in users:
            user_tab = ttk.Frame(self.notebook)
            self.notebook.add(user_tab, text=user[0])

            # Example content for user tabs
            label = tk.Label(user_tab, text=f"Settings for {user[0]}")
            label.pack(pady=10)

        # Add the General tab
        general_label = tk.Label(self.general_tab, text="General Settings")
        general_label.pack(pady=10)
