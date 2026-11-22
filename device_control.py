
import sqlite3
import os

project_path = "/content/Smart_Home_Automation_System"

db_path = os.path.join(
    project_path,
    "database",
    "smart_home.db"
)

def control_device(device_name, action):

    action = action.upper()

    if action not in ["ON", "OFF"]:
        print("Invalid action! Use ON or OFF.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE devices
        SET status = ?, last_updated = CURRENT_TIMESTAMP
        WHERE device_name = ?
    """, (action, device_name))

    if cursor.rowcount == 0:
        print("Device not found!")
        conn.close()
        return

    cursor.execute("""
        INSERT INTO device_logs (device_name, action)
        VALUES (?, ?)
    """, (device_name, action))

    conn.commit()
    conn.close()

    print(device_name, "turned", action, "successfully!")

def show_devices():

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT device_name, device_type, status
        FROM devices
    """)

    devices = cursor.fetchall()
    conn.close()

    print("\nSMART HOME DEVICE STATUS")
    print("-----------------------")

    for device in devices:
        print("Device:", device[0])
        print("Type:", device[1])
        print("Status:", device[2])
        print("-----------------------")
