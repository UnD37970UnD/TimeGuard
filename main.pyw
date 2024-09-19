import os
import sys
import privileges
import gui
import countdown

def main():
    print("[INFO] Starting the Parental Control program...")

    # Check for admin privileges before running
    if not privileges.is_admin():
        print("[INFO] No admin privileges detected. Attempting to run as admin...")
        privileges.run_as_admin()

    print("[INFO] Admin privileges verified.")

    # Initialize the GUI
    gui.run_gui()

if __name__ == "__main__":
    main()
