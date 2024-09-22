import os
import sys
import tkinter as tk
import threading
import time
from datetime import datetime
from config_screen import ConfigScreen
from admin_frame import AdminFrame
from countdown import start
from user_frame import UserFrame
from admin_panel import AdminPanel
from system_tray import create_tray_icon
from database import save_time, setup_db, is_first_run

def log_time(stop_event, interval):
    username = os.getlogin()
    while not stop_event.is_set():
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Logging current time: {current_time}")
        save_time(current_time, username)
        time.sleep(interval)


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modular Tkinter App")
        self.geometry("400x300")
        
        setup_db()

        self.frames = {}
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (ConfigScreen, AdminFrame, UserFrame, AdminPanel):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")


        self.switch_button = tk.Button(self, text="", command=self.toggle_frames)
        self.switch_button.pack(side="bottom", fill="x")


        self.stop_event = threading.Event()  


        self.first_run = is_first_run()


        if self.first_run:
            self.show_frame(ConfigScreen)
        else:
            self.show_frame(UserFrame)
            self.start_time_thread()
            start()

        self.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)

        if not self.first_run:
            self.tray_thread = threading.Thread(target=self.start_tray, daemon=True)
            self.tray_thread.start()

    def start_time_thread(self):
        interval = 60
        self.time_thread = threading.Thread(target=log_time, args=(self.stop_event, interval), daemon=True)
        self.time_thread.start()

    def start_tray(self):
        self.tray_icon = create_tray_icon(self)
        self.tray_icon.run()

    def show_frame(self, frame_class):
        current_frame = self.get_current_frame()
        if hasattr(current_frame, 'on_hide'):
            current_frame.on_hide()

        frame = self.frames[frame_class]
        frame.tkraise()

        if isinstance(frame, UserFrame):
            self.switch_button.config(text="Switch to Admin")
        elif isinstance(frame, AdminFrame):
            self.switch_button.config(text="Switch to User")

    def get_current_frame(self):
        for frame_class, frame in self.frames.items():
            if frame.winfo_ismapped():
                return frame
        return None

    def toggle_frames(self):
        if self.switch_button['text'] == "Switch to Admin":
            target_frame_class = AdminFrame
        else:
            target_frame_class = UserFrame

        self.show_frame(target_frame_class)

    def minimize_to_tray(self):
        self.withdraw()

    def restore_from_tray(self):
        self.deiconify()

    def quit_application(self):

        print("Signaling the logging thread to stop...")
        self.stop_event.set()  

        if hasattr(self, 'time_thread'):
            self.time_thread.join(timeout=1)

        if hasattr(self, 'tray_icon'):
            self.tray_icon.stop()

        print("Exiting application.")
        self.quit()
        sys.exit(0)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
