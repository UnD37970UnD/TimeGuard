import tkinter as tk
from tkinter import messagebox
import sqlite3

class ConfigScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.password_label = tk.Label(self, text="Set admin password:")
        self.password_label.pack(pady=10)

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        self.confirm_password_entry = tk.Entry(self, show="*")
        self.confirm_password_entry.pack(pady=5)

        self.submit_button = tk.Button(self, text="Submit", command=self.check_password)
        self.submit_button.pack(pady=10)

    def check_password(self):
        entered_password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if entered_password == confirm_password and entered_password != "":
            self.save_password(entered_password)
            self.controller.show_frame("UserFrame")  # Show UserFrame after setting password
        else:
            messagebox.showerror("Error", "Passwords do not match or are empty")

    def save_password(self, password):
        conn = sqlite3.connect('timeguard.db')
        cursor = conn.cursor()
        # Create table if it does not exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
                          id INTEGER PRIMARY KEY,
                          key TEXT UNIQUE,
                          value TEXT)''')
        conn.commit()
        # Store the password in the database
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", ('admin_password', password))
        conn.commit()
        conn.close()

    def on_show(self):
        # Any actions needed when this frame is shown
        pass

    def on_hide(self):
        # Any actions needed when this frame is hidden
        pass