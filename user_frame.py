import tkinter as tk

class UserFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Add content for the user frame here
        tk.Label(self, text="User Panel").pack(pady=20)

    def on_show(self):
        # Any actions needed when this frame is shown
        pass

    def on_hide(self):
        # Any actions needed when this frame is hidden
        pass