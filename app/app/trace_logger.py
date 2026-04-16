import csv
import os
from datetime import datetime

SIGHTINGS_FILE = "data/sightings.csv"


def log_sighting(camera_id, roll_no, name, score):
    """
    Logs recognized person sightings into CSV file.
    """
    os.makedirs("data", exist_ok=True)

    file_exists = os.path.exists(SIGHTINGS_FILE)

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    with open(SIGHTINGS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["Name", "Roll No", "Camera ID", "Date", "Time", "Score"])

        # ✅ CORRECT ORDER
        writer.writerow([
            name,
            roll_no,
            camera_id,
            date_str,
            time_str,
            round(score, 4)
        ])

    print(f"[TRACE] Logged: {name} ({roll_no}) on {camera_id} at {time_str}")