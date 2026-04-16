import cv2
import insightface
from app.detector import detect_and_track
from app.tracker import get_tracked_persons
from app.face_db import load_face_database
from app.recognize import recognize_face
from app.trace_logger import log_sighting

# -----------------------------
# CONFIG
# -----------------------------
CAMERA_ID = "Camera_1"
LOG_INTERVAL_SECONDS = 10   # log same person only once every 10 sec

# -----------------------------
# LOAD FACE MODEL
# -----------------------------
print("[INFO] Loading InsightFace...")
face_app = insightface.app.FaceAnalysis(name="buffalo_l")
face_app.prepare(ctx_id=0, det_size=(640, 640))

# -----------------------------
# LOAD FACE DATABASE
# -----------------------------
print("[INFO] Loading registered face database...")
face_database = load_face_database(face_app)

# -----------------------------
# START WEBCAM
# -----------------------------
print("[INFO] Starting webcam...")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("[ERROR] Could not open webcam.")
    exit()

print("[INFO] Webcam started. Press Q to quit.")

# Prevent duplicate logs every frame
last_logged_times = {}

while True:
    ret, frame = cap.read()
    if not ret:
        print("[WARNING] Failed to read frame.")
        break

    # -----------------------------
    # DETECT + TRACK PERSONS
    # -----------------------------
    results = detect_and_track(frame)
    tracked_persons = get_tracked_persons(results)

    for person in tracked_persons:
        x1, y1, x2, y2 = person["bbox"]
        track_id = person["track_id"]

        # Safety clamp
        h, w = frame.shape[:2]
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w, x2)
        y2 = min(h, y2)

        person_crop = frame[y1:y2, x1:x2]

        # -----------------------------
        # FACE RECOGNITION
        # -----------------------------
        name, roll_no, score = recognize_face(person_crop, face_app, face_database)

        label = f"{name} ({roll_no}) [{score:.2f}]"

        # Box color
        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)

        # Draw bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # -----------------------------
        # LOG SIGHTING
        # -----------------------------
        if name != "Unknown":
            current_time = cv2.getTickCount() / cv2.getTickFrequency()

            if track_id not in last_logged_times:
                last_logged_times[track_id] = 0

            if current_time - last_logged_times[track_id] > LOG_INTERVAL_SECONDS:
                log_sighting(CAMERA_ID, roll_no, name, score)
                print(f"[LOGGED] {name} ({roll_no}) at {CAMERA_ID}")
                last_logged_times[track_id] = current_time

    # Show live feed
    cv2.imshow("Surveillance System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()