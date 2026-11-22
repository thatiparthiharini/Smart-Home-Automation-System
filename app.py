
import os
import sys
from flask import Flask, render_template, request, jsonify

project_path = "/content/Smart_Home_Automation_System"
sys.path.insert(0, project_path)

from device_control import control_device, show_devices

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/devices")
def get_devices():
    import sqlite3

    db_path = os.path.join(
        project_path,
        "database",
        "smart_home.db"
    )

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT device_name, device_type, status
        FROM devices
    """)

    devices = cursor.fetchall()
    conn.close()

    return jsonify([
        {
            "name": device[0],
            "type": device[1],
            "status": device[2]
        }
        for device in devices
    ])

@app.route("/control", methods=["POST"])
def control():
    data = request.get_json()

    device_name = data.get("device_name")
    action = data.get("action")

    if not device_name or action not in ["ON", "OFF"]:
        return jsonify({"message": "Invalid request"}), 400

    control_device(device_name, action)

    return jsonify({
        "message": device_name + " turned " + action + " successfully!"
    })



@app.route("/schedule", methods=["POST"])
def schedule_device():
    from scheduler import add_schedule

    data = request.get_json()

    device_name = data.get("device_name")
    action = data.get("action")
    scheduled_time = data.get("scheduled_time")

    if not device_name or action not in ["ON", "OFF"] or not scheduled_time:
        return jsonify({"message": "Invalid schedule details"}), 400

    add_schedule(device_name, action, scheduled_time)

    return jsonify({"message": "Schedule added successfully!"})




@app.route("/schedules")
def get_schedules():
    import sqlite3

    db_path = os.path.join(project_path, "database", "smart_home.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT device_name, action, scheduled_time, executed
        FROM schedules
        ORDER BY id DESC
    """)

    records = cursor.fetchall()
    conn.close()

    return jsonify([
        {
            "device": row[0],
            "action": row[1],
            "scheduled_time": row[2],
            "executed": row[3]
        }
        for row in records
    ])


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )

@app.route("/logs")
def get_logs():
    import sqlite3

    db_path = os.path.join(
        project_path,
        "database",
        "smart_home.db"
    )

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT device_name, action, timestamp
        FROM device_logs
        ORDER BY id DESC
    """)

    records = cursor.fetchall()
    conn.close()

    return jsonify([
        {
            "device": row[0],
            "action": row[1],
            "timestamp": row[2]
        }
        for row in records
    ])
