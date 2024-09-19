import time
import threading
from plyer import notification
import os
from datetime import datetime, timedelta

def start_timer(user, total_seconds, root):
    """
    Start the timer for the user and schedule the 5-minute warning for always-on-top.
    """
    print(f"[INFO] Countdown started for {user}. Total allowed time: {total_seconds} seconds.")

    five_minute_warning = total_seconds - 300
    ten_minute_warning = total_seconds - 600

    if ten_minute_warning > 0:
        timer = threading.Timer(ten_minute_warning, notify_10_minutes_left, [user])
        timer.start()
        print(f"[INFO] 10-minute warning set to trigger in {ten_minute_warning} seconds.")

    if five_minute_warning > 0:
        five_minute_timer = threading.Timer(five_minute_warning, trigger_always_on_top, [root])
        five_minute_timer.start()
        print(f"[INFO] 5-minute warning set to trigger in {five_minute_warning} seconds.")

    # Schedule the logout event when time is up
    logout_timer = threading.Timer(total_seconds, log_out_user, [user])
    logout_timer.start()
    print(f"[INFO] User will be logged out after {total_seconds} seconds.")

def notify_10_minutes_left(user):
    """
    Send a notification to the user when there are 10 minutes remaining.
    """
    print(f"[INFO] 10-minute notification triggered for {user}.")
    notification.notify(
        title="Time Alert",
        message="You have 10 minutes left. Save your work!",
        timeout=10  # Notification display timeout
    )

def trigger_always_on_top(root):
    """
    Make the window always on top and fullscreen when 5 minutes remain.
    """
    print("[INFO] 5-minute warning triggered. Making window always on top.")
    root.attributes('-topmost', True)
    root.attributes('-fullscreen', True)
    notification.notify(
        title="Time Alert",
        message="You have 5 minutes left. The program is now on top.",
        timeout=10
    )

def log_out_user(user):
    """
    Log out the user when time is up.
    """
    print(f"[INFO] Time's up for {user}. Logging out...")
    os.system("shutdown -l")
