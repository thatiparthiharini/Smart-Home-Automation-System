
import sqlite3
import os
import time
import threading
from datetime import datetime
from zoneinfo import ZoneInfo

from device_control import control_device

project_path = "/content/Smart_Home_Automation_System"

db_path = os.path.join(
    project_path,
    "database",
    "smart_home.db"
)

TIMEZONE = ZoneInfo("Asia/Kolkata")

def add_schedule(device_name, action, scheduled_time):

    action = action.upper()

    if action not in ["ON", "OFF"]:
        print("Invalid action!")
        return

    try:
        schedule_datetime = datetime.strptime(
            scheduled_time, "%Y-%m-%d %H:%M"
        )
    except ValueError:
        print("Use format: YYYY-MM-DD HH:MM")
        return

    if schedule_datetime <= datetime.now(TIMEZONE).replace(tzinfo=None):
        print("Please select a future time!")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO schedules
        (device_name, action, scheduled_time)
        VALUES (?, ?, ?)
    """, (device_name, action, scheduled_time))

    conn.commit()
    conn.close()

    print("Schedule added successfully!")

def check_schedules():

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    current_time = datetime.now(TIMEZONE).strftime(
        "%Y-%m-%d %H:%M"
    )

    cursor.execute("""
        SELECT id, device_name, action
        FROM schedules
        WHERE scheduled_time <= ? AND executed = 0
    """, (current_time,))

    schedules = cursor.fetchall()

    for schedule in schedules:
        schedule_id, device_name, action = schedule

        control_device(device_name, action)

        cursor.execute("""
            UPDATE schedules
            SET executed = 1
            WHERE id = ?
        """, (schedule_id,))

    conn.commit()
    conn.close()

def run_scheduler():

    print("Smart Home Scheduler started!")

    while True:
        check_schedules()
        time.sleep(10)
