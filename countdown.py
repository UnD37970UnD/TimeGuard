import time
from plyer import notification
import database
import os

def start_timer(user, total_seconds):
    while total_seconds > 0:
        time.sleep(1)
        total_seconds -= 1
        # Notify when 10 minutes remain
        if total_seconds == 600:  
            notification.notify(
                title="Time Alert",
                message="You have 10 minutes left. Save your work!",
                timeout=10
            )
        # Log remaining time in database
        database.log_time(user, total_seconds)

    # Log the user out when time is up
    log_out_user()

def log_out_user():
    # Command to log out the user (Windows)
    os.system("shutdown -l")
