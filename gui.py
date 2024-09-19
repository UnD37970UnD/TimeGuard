import tkinter as tk
from tkinter import messagebox
import countdown
import database

def run_gui():
    root = tk.Tk()
    root.title("Parental Control")

    # Two panels (frames): Admin and User
    admin_frame = tk.Frame(root)
    user_frame = tk.Frame(root)

    def show_admin_panel():
        admin_frame.pack(fill="both", expand=True)
        user_frame.pack_forget()

    def show_user_panel():
        user_frame.pack(fill="both", expand=True)
        admin_frame.pack_forget()

    # Main menu to switch between admin and user
    main_menu = tk.Menu(root)
    root.config(menu=main_menu)

    panel_menu = tk.Menu(main_menu, tearoff=0)
    main_menu.add_cascade(label="Switch Panel", menu=panel_menu)
    panel_menu.add_command(label="Admin Panel", command=show_admin_panel)
    panel_menu.add_command(label="User Panel", command=show_user_panel)

    # --- Admin Panel ---
    user_var = tk.StringVar(value="Select User")
    hours_var = tk.StringVar()
    minutes_var = tk.StringVar()

    tk.Label(admin_frame, text="Admin Panel", font=("Arial", 18)).pack(pady=10)

    user_label = tk.Label(admin_frame, text="Select User:")
    user_label.pack()
    user_menu = tk.OptionMenu(admin_frame, user_var, "User1", "User2", "User3")
    user_menu.pack()

    tk.Label(admin_frame, text="Set Hours:").pack()
    tk.Entry(admin_frame, textvariable=hours_var).pack()

    tk.Label(admin_frame, text="Set Minutes:").pack()
    tk.Entry(admin_frame, textvariable=minutes_var).pack()

    def save_settings():
        user = user_var.get()
        time_limit = f"{hours_var.get()}:{minutes_var.get()}"
        print(f"[INFO] Saving settings for user: {user}, Time limit: {time_limit}")

        # Save to database
        database.save_time_limit(user, time_limit)
        database.save_login_time(user)  # Save the current time as the login time
        messagebox.showinfo("Success", "Settings saved!")

        # Start countdown timer
        total_seconds = int(hours_var.get()) * 3600 + int(minutes_var.get()) * 60
        countdown.start_timer(user, total_seconds, root)

    save_button = tk.Button(admin_frame, text="Save Settings", command=save_settings)
    save_button.pack(pady=10)

    # --- User Panel ---
    tk.Label(user_frame, text="User Panel", font=("Arial", 18)).pack(pady=10)
    remaining_time_var = tk.StringVar()
    remaining_time_label = tk.Label(user_frame, textvariable=remaining_time_var, font=("Arial", 16))
    remaining_time_label.pack()

    def update_remaining_time(remaining_seconds):
        minutes, seconds = divmod(remaining_seconds, 60)
        remaining_time_var.set(f"Time Left: {minutes:02}:{seconds:02}")

    # Show Admin Panel by default
    show_admin_panel()

    root.mainloop()
