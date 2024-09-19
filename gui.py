import tkinter as tk
from tkinter import messagebox
import countdown
import database

def run_gui():
    root = tk.Tk()
    root.title("Parental Control Setup")

    # User dropdown, Time limit input, etc.
    user_var = tk.StringVar(value="Select User")
    user_label = tk.Label(root, text="Select User:")
    user_label.grid(row=0, column=0)
    user_menu = tk.OptionMenu(root, user_var, "User1", "User2", "User3")  # Populate dynamically from system
    user_menu.grid(row=0, column=1)

    hours_var = tk.StringVar()
    minutes_var = tk.StringVar()
    tk.Label(root, text="Hours:").grid(row=1, column=0)
    tk.Entry(root, textvariable=hours_var).grid(row=1, column=1)
    tk.Label(root, text="Minutes:").grid(row=2, column=0)
    tk.Entry(root, textvariable=minutes_var).grid(row=2, column=1)

    def save_settings():
        user = user_var.get()
        time_limit = f"{hours_var.get()}:{minutes_var.get()}"
        database.save_time_limit(user, time_limit)
        messagebox.showinfo("Success", "Settings saved!")
        # Start countdown
        countdown.start_timer(user, int(hours_var.get()) * 3600 + int(minutes_var.get()) * 60)

    save_button = tk.Button(root, text="Save", command=save_settings)
    save_button.grid(row=3, columnspan=2)

    root.mainloop()
