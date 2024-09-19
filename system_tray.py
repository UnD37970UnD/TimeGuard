import pystray
from PIL import Image
from tkinter import messagebox

def create_tray_icon(app):
    image = Image.open("favicon.ico")

    def on_quit(icon, item):
        app.quit_application()

    def on_restore(icon, item):
        app.restore_from_tray()

    menu = pystray.Menu(
        pystray.MenuItem('Open', on_restore),
        pystray.MenuItem('Quit', on_quit)
    )

    icon = pystray.Icon("name", image, "App Name", menu)
    return icon
