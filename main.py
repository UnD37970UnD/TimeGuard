import tkinter as tk
import threading
from config_screen import ConfigScreen
from admin_frame import AdminFrame
from user_frame import UserFrame
from admin_panel import AdminPanel
from system_tray import create_tray_icon
from database import setup_db, is_first_run

class MainApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
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

        # Initialize switch button
        self.switch_button = tk.Button(self, text="", command=self.toggle_frames)
        self.switch_button.pack(side="bottom", fill="x")

        # Check if this is the first run
        self.first_run = is_first_run()

        # Show the correct frame based on first run status
        if self.first_run:
            self.show_frame(ConfigScreen)
        else:
            self.show_frame(UserFrame)

        self.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)

        # Only create tray icon if it's not the first run
        if not self.first_run:
            self.tray_thread = threading.Thread(target=self.start_tray, daemon=True)
            self.tray_thread.start()

    def start_tray(self):
        self.tray_icon = create_tray_icon(self)
        self.tray_icon.run()

    def show_frame(self, frame_class):
        # Call on_hide method for current frame if available
        current_frame = self.get_current_frame()
        if hasattr(current_frame, 'on_hide'):
            current_frame.on_hide()

        frame = self.frames[frame_class]
        frame.tkraise()
        
        # Update button text based on the current frame
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
        # Get the current frame and switch to the other frame
        if self.switch_button['text'] == "Switch to Admin":
            target_frame_class = AdminFrame
        else:
            target_frame_class = UserFrame

        # Show the target frame
        self.show_frame(target_frame_class)

    def minimize_to_tray(self):
        # Minimize the window to the tray but keep the app running in the tray
        self.withdraw()

    def restore_from_tray(self):
        # Restore the window when the tray icon is clicked or triggered
        self.deiconify()

    def quit_application(self):
        # Explicitly stop the tray icon and quit the application
        if hasattr(self, 'tray_icon'):
            self.tray_icon.stop()
        self.quit()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
