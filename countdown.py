import sqlite3, os
from datetime import datetime, time, timedelta
from database import get_user


def start():
    username = username = os.getlogin()
    start_countdown = datetime.now()
    time_limit = get_user(username)[3]
    finish_time = start_countdown + timedelta(minutes=time_limit)
    lock_time = None
    running = True
    print(f"Time limit: {time_limit}")
    print(f"Posible finish time: {finish_time}")
    

    