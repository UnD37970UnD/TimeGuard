import os
import sys
import privileges
import gui

def main():
    # Check for admin privileges before running
    if not privileges.is_admin():
        privileges.run_as_admin()

    # Initialize the GUI
    gui.run_gui()

if __name__ == "__main__":
    main()
