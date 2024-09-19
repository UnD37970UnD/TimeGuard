import tkinter as tk
from tkinter import messagebox
import sqlite3
from admin_panel import AdminPanel

class AdminFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=10)
        
        self.submit_button = tk.Button(self, text="Submit", command=self.check_password)
        self.submit_button.pack(pady=10)

        # Bind Enter key to the submit function
        self.bind("<Return>", lambda event: self.check_password())

    def check_password(self):
        entered_password = self.password_entry.get()
        stored_password = self.get_stored_password()

        if entered_password == stored_password:
            self.controller.show_frame(AdminPanel)
        else:
            messagebox.showerror("Error", "Incorrect password")
        self.clear_password()  # Clear password entry field

    def get_stored_password(self):
        conn = sqlite3.connect('timeguard.db')
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key='admin_password'")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else ""

    def clear_password(self):
        self.password_entry.delete(0, tk.END)  # Clear the password entry field

    def on_show(self):
        self.clear_password()  # Clear the password entry field when showing the frame

    def on_hide(self):
        pass  # Add any actions needed when this frame is hidden
