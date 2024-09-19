import ctypes
import sys
import os

def is_admin():
    """
    Check if the program is running with administrative privileges.
    Returns True if running as admin, False otherwise.
    """
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        print(f"[INFO] Admin privilege check: {is_admin}")
        return is_admin
    except:
        print("[ERROR] Unable to determine admin privileges.")
        return False

def run_as_admin():
    """
    Re-run the program with administrative privileges.
    If already an admin, do nothing. If not, it prompts for elevation.
    """
    if sys.platform == "win32":
        try:
            print("[INFO] Attempting to restart program with admin privileges...")
            params = ' '.join([f'"{arg}"' for arg in sys.argv])  # Maintain command-line arguments
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
            print("[INFO] Program elevated successfully.")
            sys.exit(0)
        except Exception as e:
            print(f"[ERROR] Failed to elevate privileges: {e}")
            raise RuntimeError("Program needs to be run with admin privileges.")
    else:
        raise RuntimeError("[ERROR] Admin privileges required. Please run as administrator on a supported platform.")
